#This function calculates the avarage of a lis of numbers

def calculate_average(numbers):
    # Ensures the list is not empty
    if len(numbers) == 0:
        return 0
        
    # Calculate the sum of the numbers of the list
    sum = 0
    for number in numbers:
        sum += number
    
    # Get the average of the list & return the value
    average = sum / len(numbers)
    return average
    
if __name__ == '__main__':
    
    number_list = [1, 23, 67, 58, 99]
    
    number_average = calculate_average(number_list)
    print(f"Average of number in the list: {number_average}")
    