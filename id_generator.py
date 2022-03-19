import re

# create a new ID as the maximum +1
# ASSUMPTION: id are written in the format {alphabetical_characters}{numerical_characters}
#             and are assigned incrementally
def next_id(str_id: str, fill_char_n : int = 4) -> str:


    prefix_search = re.search(r"^[a-z]+", str_id, re.IGNORECASE)
    count_search = re.search(r"\d+$", str_id, re.IGNORECASE)


    if prefix_search and count_search:
        prefix = prefix_search.group()
        count = int(count_search.group())
    else:
        raise ValueError(f"Unable to extract ID features, string received: {str_id}")


    return f"{prefix}" + str(count+1).rjust(fill_char_n, "0")





def main():
    print(next_id("cr0001"))
    print(next_id("parar0301"))
    try:
        print(next_id("0parar0301"))
    except ValueError:
        print("ValueError knew that")



if __name__ == "__main__":
    main()
