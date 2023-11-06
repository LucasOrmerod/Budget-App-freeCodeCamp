import math

class Category:
  def __init__(self, name):
    self.ledger = []
    self.name = name if name else "Category"

  def __str__(self):
    # Create the title line.
    line_string = ""
    length_without_name = 30 - len(self.name)
    asterisk_length_left = math.floor(length_without_name / 2)
    asterisk_length_right = math.ceil(length_without_name / 2)
    line_string += "*" * asterisk_length_left + self.name + "*" * asterisk_length_right + "\n"

    # Create the ledger lines.
    ledger_string = ""
    for dict in self.ledger:
      short_desc = dict["description"][:23]
      decimal_amount = "{:.2f}".format(round(float(dict["amount"]), 2))
      short_amount = str(decimal_amount)[:7]
      free_space = 30 - len(short_desc) - len(short_amount)

      # add the description to ledger_string.
      ledger_string += short_desc

      # Add the free space.
      for i in range(free_space):
        ledger_string += " "

      # Add the amount and a new line.
      ledger_string += short_amount + "\n"

    # Add the total at the end.
    total_string = "Total: " + str(self.get_balance())

    # Print the full chart.
    return line_string + ledger_string + total_string
  
  def deposit(self, amount, description=None):
    self.ledger.append({"amount": amount, "description": description if description \
                        else ""})
    return True

  def withdraw(self, amount, description=None):
    if not self.check_funds(amount):
      return False
    self.ledger.append({"amount": amount * -1, "description": description if \
                        description else ""})
    return True

  def get_balance(self):
    balance = 0
    for dict in self.ledger:
      balance += dict["amount"]
    return balance

  def transfer(self, amount, category):
    if not self.check_funds(amount):
      return False
    self.withdraw(amount, ("Transfer to " + category.name))
    category.deposit(amount, ("Transfer from " + self.name))
    return True
    
  def check_funds(self, amount):
    return amount <= self.get_balance()

def create_spend_chart(categories):
  output_string = "Percentage spent by category\n"

  # Get the total spend of each of the categories.
  spend_totals = {}
  for cat in categories:
    spend_totals[cat.name] = 0
    for transaction in cat.ledger:
      if transaction["amount"] < 0:
        spend_totals[cat.name] += round(abs(transaction["amount"]))

  # Get the total spend across all categories.
  total_spending = 0
  for v in spend_totals.values():
    total_spending += v

  # Get the percentage that each category represents floored to the nearest 10.
  spend_percentages = {}
  for v in spend_totals.values():
    spend_percentages[v] = (v / total_spending) * 100
  
  # Create the chart and data.
  chart_string = ""
  for i in range (10, -1, -1):
    # Add the percentage number to the left of the chart.
    chart_string += "  0|" if i == 0 else ""
    chart_string += "100|" if i == 10 else ""
    chart_string += " " + str(i * 10) + "|" if i != 0 and i < 10 else ""

    # Add an 'o' if v is more than or equal to i * 10 when rounded to the nearest 10.
    for v in spend_percentages.values():
      if math.floor(v / 10) * 10 >= i * 10:
        chart_string += " o "
      else:
        chart_string += "   " # Adds three spaces.

    # Add an extra space and a new line after the last percentage.
    chart_string += " \n"

  # Create the dashes line.
  dashes_string = "    " # Four spaces.
  for c in categories:
    dashes_string += "---"
  dashes_string += "-\n"

  # Find which category name is the longest.
  longest_name = 0
  for cat in categories:
    if len(cat.name) > longest_name:
      longest_name = len(cat.name)
      
  # Create the labels for the bottom of the chart.
  label_string = ""
  for i in range(longest_name):
    label_string += "    " # Adds four spaces.
    for cat in categories:
      if i < len(cat.name):
        label_string += " " + cat.name[i] + " "
      else:
        label_string += "   " # Adds three spaces.
    label_string += " \n"
  label_string = label_string[:-2] # Removes the trailing new line.
  label_string += " " # Adds a space in place of the new line.
    

  # Create the final output_string.
  output_string += chart_string + dashes_string + label_string
  return output_string