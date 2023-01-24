import requests
import re

#New structures can be added using this script
#Find new structures here: https://conwaylife.com/patterns/

def url_valid(urlstring):
  if ".cells" not in urlstring or "https://conwaylife.com/patterns/" not in urlstring:
    return False
  else:
    return True


#optional print for help
def print_array(array):
  for row in array:
    print(row)


def create_new_array(stri):
  new = stri.replace("O", "1").replace(".", "0").split("\n")
  final = []
  last = []

  for i in new:
    final.append(list(i))

  for j in range(len(final)):
    last.append([])
    for h in range(len(final[j])):
      integer = int(final[j][h])
      last[j].append(integer)
  return (last)


def find_longest_array_item(my_array):
  # initialize a variable to store the length of the longest item
  longest = 0

  # iterate through the items in the array
  for item in my_array:
    # check if the length of the current item is greater than the current longest
    if len(item) > longest:
      # update the longest variable with the length of the current item
      longest = len(item)

  # print the length of the longest item
  return (longest)


def lengthen_array_items(array, desired_length):
  for row in array:
    while len(row) != desired_length:
      row.append(0)
  return array


def urltoinput():
  print(
    "Enter a url to a .cells project from the collection at https://conwaylife.com/patterns/"
  )
  while True:
    url = str(input("URL: "))
    print("\n")
    if url_valid(url) == True:
      break
    else:
      print(
        "Please enter a valid url to a pattern from https://conwaylife.com/patterns/. Make sure it is a .cells pattern \n"
      )

  #get text from conwaylife url
  pagedata = requests.get(url)

  #isolate the cells
  new_string = re.sub(r"^!.*\n", "", pagedata.text, flags=re.MULTILINE)
  new_string = new_string.replace('\r', '')

  #create the array
  first_version = create_new_array(new_string)
  final_version = lengthen_array_items(first_version,
                                       find_longest_array_item(first_version))
  return (final_version)