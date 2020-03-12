# The program of cinema - assignment 3
import sys

alpha = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z')


def creating_hall(hall_dict, hall_name, row, column):
    hall_dict[hall_name] = []
    lst = list()
    for j in range(column):
        lst.append('X')
    hall_dict[hall_name] = {}
    for i in range(row):
        hall_dict[hall_name][alpha[i]] = (lst[:])


def dig_num(x):
    # This function assumes that x is positive integer
    acc = 1
    while x>9:
        acc += 1
        x = int(x / 10)
    return acc


# opening input file and parsing commands
fh = open(sys.argv[1], 'r')
fo = open("out.txt", 'w')
commands = fh.readlines()

# stripping newline characters from end of lines
for c in range(len(commands)):
    commands[c] = commands[c][:-1]

halls = dict()
for i in commands:
    if i.split()[0] == 'CREATEHALL':
        if len(i.split()) < 3:
            print("Error: Not enough parameters for creating a hall!")
            fo.write("Error: Not enough parameters for creating a hall!\n")
            continue
        elif len(i.split()) > 3:
            print("Error: Too much parameters for creating a hall!")
            fo.write("Error: Too much parameters for creating a hall!\n")
            continue

        if int(i.split()[2].split('x')[0]) <= 0 and int(i.split()[2].split('x')[1]) <= 0:
            print("Error: Dimension values of hall must be positive integer!")
            fo.write("Error: Dimension values of hall must be positive integer!\n")
            continue

        if i.split()[1] in halls:
            print("Warning: Cannot create the hall for the second time. The cinema has already", i.split()[1])
            fo.write("Warning: Cannot create the hall for the second time. The cinema has already %s\n" %(i.split()[1]))
            continue

        if len(i.split()[-1].split('x')) > 2 or len(i.split()[-1].split('x')) < 2:
            print("Error: The dimension that you entered is not supported!")
            fo.write("Error: The dimension that you entered is not supported!\n")
            continue

        x, y = int(i.split()[-1].split('x')[0]), int(i.split()[-1].split('x')[1])
        creating_hall(halls, i.split()[1], x, y)
        print("Hall '" + i.split()[1] + "' having", x*y, "seats has been created")
        fo.write("Hall '%s' having %s seats has been created\n" %(i.split()[1], str(x*y)))

    elif i.split()[0] == 'SELLTICKET':
        if len(i.split()) < 5:
            print("Error: Not enough parameters for selling a ticket!")
            fo.write("Error: Not enough parameters for selling a ticket!\n")
            continue

        try:
            for seat in i.split()[4:]:
                if seat[0] in halls[i.split()[3]]:
                    if '-' in seat:
                        if (int(seat.split('-')[0][1:]) >= 0) and (
                                int(seat.split('-')[0][1:]) < len(halls[i.split()[3]]['A'])) and (
                                int(seat.split('-')[1]) >= 0) and (
                                int(seat.split('-')[1]) < len(halls[i.split()[3]]['A'])):
                            x, y = int(seat.split('-')[0][1:]), int(seat.split('-')[-1])
                            for j in range(x, y):
                                if halls[i.split()[3]][seat[0]][j] == 'X':
                                    pass
                                else:
                                    break
                            if j == y - 1:
                                for j in range(x, y):
                                    if i.split()[2] == 'student':
                                        halls[i.split()[3]][seat[0]][j] = 'S'
                                    elif i.split()[2] == 'full':
                                        halls[i.split()[3]][seat[0]][j] = 'F'
                            else:
                                print(
                                    "Warning: The seats %s cannot be sold to %s due some of them have already been sold"
                                    % (seat, i.split()[1]))
                                fo.write(
                                    "Warning: The seats %s cannot be sold to %s due some of them have already been sold\n"
                                    % (seat, i.split()[1]))
                                continue
                            print("Success: %s has bought %s at %s" % (i.split()[1], seat, i.split()[3]))
                            fo.write("Success: %s has bought %s at %s\n" % (i.split()[1], seat, i.split()[3]))
                        else:
                            print("Error: The hall '%s' has less column than the specified index %s!"
                                  % (i.split()[3], seat))
                            fo.write("Error: The hall '%s' has less column than the specified index %s!\n"
                                     % (i.split()[3], seat))

                    else:
                        if (int(seat[1:]) >= 0) and (int(seat[1:]) < len(halls[i.split()[3]]['A'])):
                            if halls[i.split()[3]][seat[0]][int(seat[1:])] == 'S' or halls[i.split()[3]][seat[0]][int(seat[1:])] == 'F':
                                print("Warning: The seat %s cannot be sold to %s since it was already sold!" % (
                                    seat, i.split()[1]))
                                fo.write("Warning: The seat %s cannot be sold to %s since it was already sold!\n" % (
                                    seat, i.split()[1]))
                            elif halls[i.split()[3]][seat[0]][int(seat[1:])] == 'X':
                                if i.split()[2] == 'student':
                                    halls[i.split()[3]][seat[0]][int(seat[1:])] = 'S'
                                elif i.split()[2] == 'full':
                                    halls[i.split()[3]][seat[0]][int(seat[1:])] = 'F'
                                print("Success: %s has bought %s at %s" % (i.split()[1], seat, i.split()[3]))
                                fo.write("Success: %s has bought %s at %s\n" % (i.split()[1], seat, i.split()[3]))
                        else:
                            print("Error: The hall '%s' has less column than the specified index %s!"
                                  % (i.split()[3], seat))
                            fo.write("Error: The hall '%s' has less column than the specified index %s!\n"
                                     % (i.split()[3], seat))
                else:
                    print("Error: The hall '%s' has less row than the specified index %s!"
                          % (i.split()[3], seat))
                    fo.write("Error: The hall '%s' has less row than the specified index %s!\n"
                             % (i.split()[3], seat))
        except KeyError:
            print("Error: There is some key error. Be sure that you correctly entered customer name, fare type and hall name, please.")
            fo.write("Error: There is some key error. Be sure that you correctly entered customer name, fare type and hall name, please.\n")

    elif i.split()[0] == 'CANCELTICKET':
        if len(i.split()) < 3:
            print("Error: Not enough parameters for canceling a ticket!")
            fo.write("Error: Not enough parameters for canceling a ticket!\n")
            continue

        try:
            for seat in i.split()[2:]:
                if seat[0] in halls[i.split()[1]]:
                    if '-' in seat:
                        if (int(seat.split('-')[0][1:]) >= 0) and (
                                int(seat.split('-')[0][1:]) < len(halls[i.split()[1]]['A'])) and (
                                int(seat.split('-')[1]) >= 0) and (
                                int(seat.split('-')[1]) < len(halls[i.split()[1]]['A'])):
                            for j in range(x, y):
                                if halls[i.split()[1]][seat[0]][j] == 'S' or halls[i.split()[1]][seat[0]][j] == 'F':
                                    pass
                                else:
                                    break
                            if j == y - 1:
                                for j in range(x, y):
                                    halls[i.split()[1]][seat[0]][j] = 'X'
                                print("Success: The seats %s at '%s' have been canceled and now ready to be sold again" %(seat, i.split()[1]))
                                fo.write("Success: The seats %s at '%s' have been canceled and now ready to be sold again\n" % (seat, i.split()[1]))
                            else:
                                x, y = int(seat.split('-')[0][1:]), int(seat.split('-')[-1])
                                for j in range(x, y):
                                    if halls[i.split()[1]][seat[0]][j] == 'S' or halls[i.split()[1]][seat[0]][j] == 'F':
                                        halls[i.split()[1]][seat[0]][j] = 'X'
                                        print(
                                            "Success: The seat %s at %s has been canceled and now ready to sell again" % (
                                                seat, i.split()[1]))
                                        fo.write(
                                            "Success: The seat %s at %s has been canceled and now ready to sell again\n" % (
                                                seat, i.split()[1]))
                                    elif halls[i.split()[1]][seat[0]][j] == 'X':
                                        print("Error: The seat %s at %s has already been free! Nothing to cancel" % (
                                            seat, i.split()[1]))
                                        fo.write(
                                            "Error: The seat %s at %s has already been free! Nothing to cancel\n" % (
                                                seat, i.split()[1]))
                        else:
                            print("Error: The hall '%s' has less column than the specified index %s!"
                                  % (i.split()[1], seat))
                            fo.write("Error: The hall '%s' has less column than the specified index %s!\n"
                                     % (i.split()[1], seat))

                    else:
                        if (int(seat[1:]) >= 0) and (int(seat[1:]) < len(halls[i.split()[1]]['A'])):
                            if halls[i.split()[1]][seat[0]][int(seat[1:])] == 'S' or halls[i.split()[1]][seat[0]][
                                int(seat[1:])] == 'F':
                                halls[i.split()[1]][seat[0]][int(seat[1:])] = 'X'
                                print("Success: The seat %s at %s has been canceled and now ready to sell again" % (
                                seat, i.split()[1]))
                                fo.write(
                                    "Success: The seat %s at %s has been canceled and now ready to sell again\n" % (
                                    seat, i.split()[1]))
                            elif halls[i.split()[1]][seat[0]][int(seat[1:])] == 'X':
                                print("Error: The seat %s at %s has already been free! Nothing to cancel" % (
                                seat, i.split()[1]))
                                fo.write("Error: The seat %s at %s has already been free! Nothing to cancel\n" % (
                                seat, i.split()[1]))
                        else:
                            print("Error: The hall '%s' has less column than the specified index %s!" % (
                            i.split()[1], seat))
                            fo.write("Error: The hall '%s' has less column than the specified index %s!\n" % (
                            i.split()[1], seat))
                else:
                    print("Error: The hall '%s' has less row than the specified index %s!" % (i.split()[1], seat))
                    fo.write("Error: The hall '%s' has less row than the specified index %s!\n" % (i.split()[1], seat))
        except KeyError:
            print("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please." %i.split()[1])
            fo.write("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please.\n" %i.split()[1])


    elif i.split()[0] == 'BALANCE':
        if len(i.split()) < 2:
            print("Error: Not enough parameters to show balance!")
            fo.write("Error: Not enough parameters to show balance!\n")
            continue

        for hall in i.split()[1:]:
            try:
                sum_s, sum_f = 0, 0
                for row in halls[hall]:
                    for column in halls[hall][row]:
                        if column == 'S':
                            sum_s += 1
                        elif column == 'F':
                            sum_f += 1
                print("Hall report of '%s'" % (hall))
                fo.write("Hall report of '%s'\n" % (hall))
                for a in range(len("Hall report of ''") + len(hall)):
                    print("-", end='')
                    fo.write("-")
                print("\nSum of students = %s, Sum of full fares = %s, Overall = %s" % (
                    str(sum_s * 5), str(sum_f * 10), str(sum_s * 5 + sum_f * 10)))
                fo.write("\nSum of students = %s, Sum of full fares = %s, Overall = %s\n" % (
                    str(sum_s * 5), str(sum_f * 10), str(sum_s * 5 + sum_f * 10)))
            except KeyError:
                print("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please."%hall)
                fo.write("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please.\n" %hall)

    elif i.split()[0] == 'SHOWHALL':
        try:
            digit = dig_num(len(halls[i.split()[1]]['A']))
            desc_y = sorted(halls[i.split()[1]].keys(), reverse=True)

            print("Printing hall layout of", i.split()[1])
            fo.write("Printing hall layout of %s\n" % i.split()[1])

            for y in desc_y:
                print(y + " ", end='')
                fo.write("%s " % y)
                for x in range(len(halls[i.split()[1]]['A'])):
                    print(halls[i.split()[1]][y][x] + " " * digit, end='')
                    fo.write("%s%s" % (halls[i.split()[1]][y][x], " " * digit))
                print()
                fo.write("\n")
            print(" " * 2, end='')
            fo.write("%s" % " " * 2)
            for y in range(len(halls[i.split()[1]]['A'])):
                print(y, end='')
                print(" " * (digit - dig_num(y + 1) + 1), end='')
                fo.write("%s%s" % (y, " " * (digit - dig_num(y + 1) + 1)))
            print()
            fo.write("\n")
        except KeyError:
            print("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please." % i.split()[1])
            fo.write("Error: There is some key error. Be sure that you correctly entered the hall name (%s), please.\n" % i.split()[1])

    else:
        print("Error: The command that you entered is invalid")
        fo.write("Error: The command that you entered is invalid\n")
fh.close()
fo.close()