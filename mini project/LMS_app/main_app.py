from controller import controller
from client_main import menus

print("Please choose an option:")
print("1. Use Menus")
print("2. Use Controller")
print("3. Exit")

choice = int(input("Enter your choice (1/2/3): "))

if choice == 1:
    menus()
elif choice == 2:
    controller()
else:
    print("Invalid choice. Please try again.")
