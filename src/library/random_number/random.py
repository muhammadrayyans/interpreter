from datetime import datetime
import numpy as np # type: ignore
import logging
logger = logging.getLogger(' random_number')
logger.setLevel(logging.DEBUG)
from numbers import Number


class Random:
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop
        pass
    
    def __power_calculator(self, x: int | float, n: int):
        if n < 0:
            result: int | float = 1
            for i in range(n*-1):
                result*=x 
            return 1/result
        else:
            result: int | float = 1
            for i in range(n):
                result*=x 
            return result
        
    

    
    def __transform(self, x: int, code: int) -> int | None:
        low: int = min(self.start, self.stop)
        high: int = max(self.start, self.stop)
        if code == -1:
            euler_number = self.__power_calculator(2.718, -(x*x))
            middle = (low+high)/2
            formula = int(middle+(high - middle)*euler_number)
            return formula
        else:
            euler_number = self.__power_calculator(2.718, -x if code == 0 else x)
            formula = int(low + ((high-low)/(1+euler_number)))
            return formula
    
    def __clamping(self, x: int) -> int:
        
        main_host: datetime = datetime.now()
        split_set: str = str(main_host)[-6:]

        x -= int(split_set[3])
        low: int = min(self.start, self.stop)
        high: int = max(self.start, self.stop)
        return max(low, min(x, high))
    
    def execute(self):
        array: list = []
        main_host: datetime = datetime.now()
        split_set: str = str(main_host)[-6:]
        for x in split_set:
            array.append(int(x))
        numpy_array: np.ndarray = np.array(array) 
        formatted_clamper = np.vectorize(self.__clamping)
        formatted_transformer = np.vectorize(self.__transform)
        
        result_value_clamped = formatted_clamper(numpy_array)
        result_value_transformed_high = formatted_transformer(result_value_clamped ,0)
        result_value_transformed_low = formatted_transformer(result_value_clamped, 1)
        result_value_transformed_middle = formatted_transformer(result_value_clamped, -1)
        main_matrix: np.ndarray = np.array([result_value_transformed_low, 
                                      result_value_transformed_high, 
                                      result_value_transformed_middle,
                                      result_value_transformed_low, 
                                      result_value_transformed_high,
                                      result_value_transformed_middle]) 
        for i in range(0,6,2):
            for j in range(0,6,2):
                    main_matrix[i+1][j] , main_matrix[i][j] = main_matrix[i][j], main_matrix[i+1][j]
        for i in range(0,6,2):
            for j in range(0,6,2):
                    main_matrix[j][i+1] , main_matrix[j][i] = main_matrix[j][i], main_matrix[j][i+1]
        for i in range(2,6,1):
            for j in range(2,6,1):
                    main_matrix[i-2][j] , main_matrix[i][j] = main_matrix[i][j], main_matrix[i-2][j]
        for i in range(2,6,1):
            for j in range(2,6,1):
                    main_matrix[j][i-2] , main_matrix[j][i] = main_matrix[j][i], main_matrix[j][i-2]
                    
        value_x = Random(0,5).__transform(self.__clamping(self.start - array[3]), -1)
        value_y = Random(0,5).__transform(self.__clamping(self.stop) - array[5], 0)
        print(f'{value_x} {value_y}')
        print(main_matrix)
        print(main_matrix[value_x][value_y])
    
obj = Random(22, 40)
obj.execute()