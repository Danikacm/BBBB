import time

class BingoBoardGenerator:
    def __init__(self):
        self.current_seed = None

    def generate_seed(self):
        self.current_seed = int(time.time_ns()) 

    def generate_board(self):
        self.generate_seed()  

       
        columns = {
            'B': self.generate_column(1, 15),
            'I': self.generate_column(16, 30),
            'N': self.generate_column(31, 45),
            'G': self.generate_column(46, 60),
            'O': self.generate_column(61, 75)
        }
        
        board = []
        for i in range(5):
            row = []
            for key, nums in columns.items():
                if i == 0:  
                    row.append(key)
                else:
                    row.append(' ' if key == 'N' and i == 2 else nums.pop(0))
            board.append(row)

        return board

    def generate_column(self, start, end):
      
        nums = list(range(start, end + 1))
        nums = self.custom_shuffle(nums)
        return nums

    def custom_shuffle(self, nums):
        seed = self.current_seed
        for i in range(len(nums) - 1, 0, -1):
            seed = (seed * 1103515245 + 12345) % 59894879879867
            j = seed % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        return nums

def main():
    generator = BingoBoardGenerator()
    num_boards = int(input("¿Cuántos tableros deseas generar?: "))
    for i in range(num_boards):
        board = generator.generate_board()
        print(f"Tablero {i + 1}:")
        for row in board:
            print(row)

if __name__ == "__main__":
    main()