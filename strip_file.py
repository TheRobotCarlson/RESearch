results = []
result_set = set()
with open('data_files/allenz.txt') as input_file:
    temp_entry = []
    for line in input_file:
        temp_str = line.strip()
        clipped_str = temp_str[3:]

        if temp_str[:3] == "<1>":
            temp_entry = []
            temp_entry.append(clipped_str)
        elif temp_str[:3] == "<5>":
            if "?" in clipped_str or "," in clipped_str:
                continue

            cleave_num = clipped_str.find("(")

            nums = None

            if cleave_num != -1:
                cleave_num_end = clipped_str.find(")")
                nums = (clipped_str[cleave_num + 1:cleave_num_end]).split("/")
                clipped_str = clipped_str[:cleave_num]

            if clipped_str in result_set:
                continue
            result_set.add(clipped_str)
            if "^" not in clipped_str:
                clipped_str = "^" + clipped_str + "^"
            temp_entry.append(clipped_str)
            results.append(temp_entry)
            temp_entry = []

results = sorted(results, key=lambda x: len(x[1]))
with open('data_files/allenz_altered.txt', 'w+') as input_file:
    for result in results:
        input_file.write(result[0] + "," + result[1] + "\n")
