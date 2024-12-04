from werkzeug.security import generate_password_hash,check_password_hash

a = [('RF-2907', 'rauf', 'pbkdf2:sha256:260000$yhhaw29f7qqo2R7P$cd72483cf75d5b3c774029adc50b9de7d22df9dae609be4c9c5c3fef8ac3409e', '0'), ('SV-1312', 'siva', 'pbkdf2:sha256:260000$9IhzFkGUA7UYE25U$7b9afb67ee97d596e861637c7678632136640aa5099605bd31115fb14198d256', '0'), ('VK-2510', 'venkat', 'pbkdf2:sha256:260000$MppZuA43JmVUBerN$7947b6b4008bdcdca66f95465087d2c990e6ac0cf978c8e6497d900e8025619f', '0'), ('KR-0010', 'karthi', 'pbkdf2:sha256:260000$mVYpx8DxJV9pcaST$588abbb4e8dd040f5dff13591758a35b65f99c9a324ebe3058a651cba9913d49', '0')]
# l=[]
# x=0
# for i in a:
#     if "venkat" in i[1]:
#         x+=1
#         if check_password_hash(i[2],"vk25107") == True:
#             print("Welcome User!")
#         else:
#             print("Invalid Password, Please try again")
        
# if x==0:
#     print("This Username does not exist!")

### Passwords for other users: ###
# siva --> sv1312   #
# venkat --> vk2510 #
# karthi --> kr0010 #

