import pickle
import sys
from datetime import date


class Owner:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def __str__(self):
        return f"{self.name} | {self.address}"


class Pet:
    def __init__(self,
                 pet_name: str,
                 dob: date,
                 birth_weight: float,
                 name: str,
                 address: str):
        if birth_weight <= 0:
            print('Invalid value for birth weight')
            sys.exit(0)
        self.pet_name = pet_name
        self.dob = dob
        self.birth_weight = birth_weight
        self.owner = Owner(name, address)

    def __str__(self):
        return f"{self.pet_name} | {self.dob} | {self.birth_weight} | {self.owner.name} | {self.owner.address}"

    def days_since_birth(self) -> int:
        return (date.today() - self.dob).days


class Mammal(Pet):
    def __init__(self,
                 pet_name: str,
                 dob: date,
                 birth_weight: float,
                 name: str,
                 address: str,
                 litter_size: int,
                 has_claws: bool):
        super().__init__(pet_name, dob, birth_weight, name, address)
        self.litter_size = litter_size
        self.has_claws = has_claws

    def __str__(self):
        return f"{self.pet_name} | {self.dob} | {self.birth_weight} | {self.owner.name} | {self.owner.address}\
                     | {self.litter_size} | {self.has_claws}"

    def compute_current_weight(self, days_since_birth: int) -> float:
        return self.birth_weight * pow(1.1, min(days_since_birth, 300) // 60)


class Fish(Pet):
    def __init__(self,
                 pet_name: str,
                 dob: date,
                 birth_weight: float,
                 name: str,
                 address: str,
                 scale: str,
                 length: float):
        super().__init__(pet_name, dob, birth_weight, name, address)
        self.scale = scale
        self.length = length

    def __str__(self):
        return f"{self.pet_name} | {self.dob} | {self.birth_weight} | {self.owner.name} | {self.owner.address}\
                     | {self.scale} | {self.length}"

    def compute_current_weight(self, days_since_birth: int) -> float:
        return self.birth_weight * pow(1.05, min(days_since_birth, 240) // 80)


class Amphibian(Pet):
    def __init__(self,
                 pet_name: str,
                 dob: date,
                 birth_weight: float,
                 name: str,
                 address: str,
                 num_limbs: int,
                 is_venomous: bool):
        super().__init__(pet_name, dob, birth_weight, name, address)
        self.num_limbs = num_limbs
        self.is_venomous = is_venomous

    def __str__(self):
        return f"{self.pet_name} | {self.dob} | {self.birth_weight} | {self.owner.name} | {self.owner.address}\
                     | {self.num_limbs} | {self.is_venomous}"

    def compute_current_weight(self, days_since_birth: int) -> float:
        curr_weight = min(self.birth_weight * 1.05**3 * 1.03**(days_since_birth//120),
                          self.birth_weight * 1.05**(days_since_birth//120))
        return curr_weight


def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    expected = " or ".join((
                        ", ".join(str(x) for x in range_[:-1]),
                        str(range_[-1])
                    ))
                    print(template.format(expected))
        else:
            return ui


class PetsInventoryApplication:
    def __init__(self):
        self.pet_data = self.load_pet_data()

    def load_pet_data(self):
        try:
            with open('petdata.dat', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def save_pet_data(self):
        with open('petdata.dat', 'wb') as file:
            pickle.dump(self.pet_data, file)

    def run(self):
        while True:
            print(
                """==== Menu ====
                1. To add a pet
                2. To print pet information for all pet in the database
                3. To print pet name and current weight of all pets in the database
                4. To print pet name, owner name and owner address for all owners with more than one pet
                5. To exit program""")
            choice = sanitised_input("Your selection: ", int, 1, 5)

            if choice == 1:
                pet_type = sanitised_input("Type of Pet? (1-Mammal;2-Fish;3-Amphibian) : ", int, 1, 3)
                print("Adding a pet")

                pet_name_ = sanitised_input("Enter the pet's name: ", str)
                dob_yyyy = sanitised_input("Enter the pet's year of birth: ", int, 1900, 2023)
                dob_mm = sanitised_input("Enter the pet's month of birth: ", int, 1, 12)
                dob_dd = sanitised_input("Enter the pet's day of birth: ", int, 1, 31)
                birth_weight_ = sanitised_input("Enter the birth weight for the pet in ounces: ", float, 0)
                owner_name = sanitised_input("Enter owner name: ", str)
                owner_address = sanitised_input("Enter owner address: ", str)
                dob_ = date(dob_yyyy, dob_mm, dob_dd)

                if pet_type == 1:  # Mammal
                    litter_size_ = sanitised_input("Enter litter size: ", int, 0)
                    has_claws_ = sanitised_input("Does the pet have claws? Enter 'y' or 'n': ", str,
                                                 range_=['y', 'n'])
                    pet = Mammal(pet_name_, dob_, birth_weight_, owner_name, owner_address, litter_size_, has_claws_)
                    self.pet_data.append(pet)
                elif pet_type == 2:  # Fish
                    scale_ = sanitised_input("Enter the scale condition. Only 'smooth' or 'rough' is allowed: ",
                                             str, range_=["smooth", "rough"])
                    length_ = sanitised_input("Enter the length of pet in inches: ", int, 0)
                    pet = Fish(pet_name_, dob_, birth_weight_, owner_name, owner_address, scale_, length_)
                    self.pet_data.append(pet)
                elif pet_type == 3:  # Amphibian
                    num_limbs_ = sanitised_input("Enter the number of limbs for the pet: ", int, 0)
                    is_venomous_ = sanitised_input("Is the pet venomous? Enter 'y' or 'n': ", str,
                                                   range_=['y', 'n'])
                    pet = Amphibian(pet_name_, dob_, birth_weight_, owner_name, owner_address, num_limbs_, is_venomous_)
                    self.pet_data.append(pet)
                print("Pet added to database")

            elif choice == 2:
                mammals_list = [pet for pet in self.pet_data if isinstance(pet, Mammal)]
                fish_list = [pet for pet in self.pet_data if isinstance(pet, Fish)]
                amphibians_list = [pet for pet in self.pet_data if isinstance(pet, Amphibian)]

                print("========================================================================")
                print("Data of all Mammals in the database")
                print("========================================================================")
                print("Pet Name | DOB | Birth Weight | Owner Name | Owner Address | Litter Sizes | Has Claws")
                for pet in mammals_list:
                    print(pet)
                print("========================================================================")
                print("Data of all Fish in the database")
                print("========================================================================")
                print("Pet Name | DOB | Birth Weight | Owner Name | Owner Address | Scale Condition | Length")
                for pet in fish_list:
                    print(pet)
                print("========================================================================")
                print("Data of all Amphibians in the database")
                print("========================================================================")
                print("Pet Name | DOB | Birth Weight | Owner Name | Owner Address | Number of Limbs | Is Venomous")
                for pet in amphibians_list:
                    print(pet)

            elif choice == 3:
                print("===============================================================")
                print("Pet name and current weights of all pets")
                print("===============================================================")
                for pet in self.pet_data:
                    days_since_birth = pet.days_since_birth()
                    current_weight = pet.compute_current_weight(days_since_birth)
                    print(f"{pet.pet_name}'s cur_weight in pounds is {current_weight/16:.2f}")

            elif choice == 4:
                print("===============================================================")
                print("Pet name - Owner name - Owner address for multi-pet owner")
                print("===============================================================")
                owner_pet_count = {}

                for pet in self.pet_data:
                    owner_name = pet.owner.name
                    owner_address = pet.owner.address
                    owner_pet_count[owner_name] = list([owner_pet_count.get(owner_name, list([0, ""]))[0] + 1,
                                                        owner_address])

                for owner_name, pet_count_address in owner_pet_count.items():
                    if pet_count_address[0] > 1:
                        print(f"{owner_name} lives in {pet_count_address[1]} and has {pet_count_address[0]} pets. The pet names are:")
                        for pet in self.pet_data:
                            if pet.owner.name == owner_name:
                                print(f"  - {pet.pet_name}")
                        print()

            elif choice == 5:
                print("You chose to exit the program")
                exit_program = sanitised_input("Are you sure (Y/N)? ", str, range_=['y', 'n', 'Y', 'N'])
                if exit_program.lower() == 'y':
                    self.save_pet_data()
                    break

            else:
                print("Invalid selection. Please enter appropriate number.")


if __name__ == "__main__":
    app = PetsInventoryApplication()
    app.run()
