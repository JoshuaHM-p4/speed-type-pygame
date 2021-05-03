## Testing Global Variables work in nested function
# from time import sleep
# def foo():
#     global x
#     x = True

#     def function():
#         global x
#         print('function called')
#         x = False
    
#     for i in range(2):
#         print(x)
#         function()
#         sleep(1)

# foo()

## Testing decorator functions
# s = None

# def with_setup(func):
#     def inner(*args, **kwargs):
#         func(*args, **kwargs)
#         print(kwargs)
#     return inner

# @with_setup
# def load(file, difficulty):
#     print('Function called')
#     s = file
#     b = difficulty 

# load('lmao.txt', difficulty = 'hard')