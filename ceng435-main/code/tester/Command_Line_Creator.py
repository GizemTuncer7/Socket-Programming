import os

class Command_Line_Creator:
    interface = None
    command = None
    distortions = None

    def __init__(self, interface="eth0", distortions=[]):
        self.interface = interface
        self.command = self.get_reset_command()
        self.distortions = distortions

    def run_command(self):
        os.system(self.command)

    def get_commands(self):
        return self.commands
    
    def set_command(self, command):
        self.command = command

    def set_interface(self, interface):
        self.interface = interface

    def get_reset_command(self):
        return f"tc qdisc del dev {self.interface} root"
    
    def reset_command(self):
        self.command = self.get_reset_command()

    def get_command_with_distortion(self, change_or_add, distortion, *args):
        change_or_add_part = f"tc qdisc {change_or_add} dev {self.interface} root netem"
        distortion_part = f"{distortion}"
        args_part = " ".join(args)

        return f"{change_or_add_part} {distortion_part} {args_part}"

    def add_distortion(self, distortion, *args):
        if distortion in self.distortions:
            change_or_add = "change"
        else:
            change_or_add = "add"
            self.distortions.append(distortion)
        
        self.command = self.get_command_with_distortion(change_or_add, distortion, *args)

    def remove_distortion(self, distortion):
        self.command = self.get_command_with_distortion("change", distortion)

        if distortion in self.distortions:
            self.distortions.remove(distortion)
        else:
            print("Distortion is not in the list of distortions")

    def add_delay(self, delay, threshold=10, distribution="uniform"):
        self.add_distortion("delay", f"{delay}ms {threshold}ms distribution {distribution}")

    def apply_loss(self, percentage):
        self.add_distortion("loss", f"{percentage}%")
    
    def apply_corruption(self, percentage):
        self.add_distortion("corrupt", f"{percentage}%")
    
    def apply_duplicate(self, percentage):
        self.add_distortion("duplicate", f"{percentage}%")

        


    


    