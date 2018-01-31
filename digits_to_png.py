 #!/usr/bin/python
 #coding=utf-8
from mnist import MNIST
import sys
import png
import random
import numpy 
import time 

ERR_SPACING = 'Spacing is invalid!!'
ERR_DIGIT_NUM = 'Invalid digit number!!'
ERR_PRODUCT_IMAGE_SUCCESS = 'Produce image sucess!!'
ERR_PRODUCT_IMAGE_FAIL = 'Produce image fail!!'
ERR_SUCCESS = 'Succuss!!' 
MAX_SAPCING = 200
MAX_DIGIT_NUM = 1000
##################################################################################
##  Class used for handle the mnist data
##################################################################################
class mnist_data():
    ##################################################################################
    ## initialize mnist file path and the samples for storing patterns of digits(0-9)
    ## input: self, file path
    ## output: None
    ##################################################################################
    def __init__(self):
        self.sample_0 = []
        self.sample_1 = []
        self.sample_2 = []
        self.sample_3 = []
        self.sample_4 = []
        self.sample_5 = []
        self.sample_6 = []
        self.sample_7 = []
        self.sample_8 = []
        self.sample_9 = []
        self.sample_map = [
            self.sample_0,
            self.sample_1,
            self.sample_2,
            self.sample_3,
            self.sample_4,
            self.sample_5,
            self.sample_6,
            self.sample_7,
            self.sample_8,
            self.sample_9,
        ]

        self.__data_is_load = 0

    ##################################################################################
    ## get sample from mnist file
    ## input: self
    ## output: None
    ##################################################################################
    def get_sample_from_file(self):
        if self.__data_is_load == 1:
            return
        mndata = MNIST('./data/')
        images, labels = mndata.load_training()
        for index in range(len(labels)):
            item = labels[index]
            sample = images[index]
            self.sample_map[item].append(sample)
        self.__data_is_load = 1

##################################################################################
##  Class used for handle the png image
##################################################################################
class png_handler():
    ##################################################################################
    ## initialize the variables for png handler
    ## input: self
    ## output: None
    ##################################################################################
    def __init__(self):
        self.__image_base_width = 28
        self.image_default_height = 28

    ##################################################################################
    ## produce the png image file
    ## input: self, image data, image width, image height(default:28)
    ## output: error message
    ##################################################################################
    def output_to_image(self, data,width,height = 28):
        now_time = time.time()
        milisecond = int((now_time - int(now_time))*1000)
        file_name = './result/image-' + time.strftime("%Y%m%d-%H-%M-%S", time.localtime()) + '-' + str(milisecond) + '.png'
        try:
            pngfile = open(file_name, 'wb')      # binary mode is important
            # scaler = preprocessing.MinMaxScaler()
            # data = scaler.fit(data)
            pngWriter = png.Writer(width, height, greyscale=True)
            pngWriter.write(pngfile,data)
            pngfile.close()
            return 0, ERR_PRODUCT_IMAGE_SUCCESS,file_name
        except:
            return -1, ERR_PRODUCT_IMAGE_FAIL,''

##################################################################################
## Class used to valid parameters
##################################################################################
class params_valid():
    ##################################################################################
    ## initialize the variables for params_valid
    ## input: self
    ## output: None
    ##################################################################################
    def __init__(self):
        self.__image_base_width = 28
    ##################################################################################
    ## valid the digit list
    ## input: self, digits (list)
    ## output: result, error message, processed digits 
    ##################################################################################
    def valid_digits(self, digits):
        processed_digits = []
        for item in digits:
            try: 
                digit = int(item)
                if digit >= 0 and digit < 10:
                    processed_digits.append(digit)
            except:
                continue
        digits_num = len(processed_digits)
        if digits_num == 0 or digits_num > MAX_DIGIT_NUM:
            return -1, ERR_DIGIT_NUM, []
        return 0, ERR_SUCCESS, processed_digits

    ##################################################################################
    ## valid the spacing
    ## input: self, spacing
    ## output: result, error message, processed spacing
    ##################################################################################
    def valid_spacing(self, spacing):
        processed_spacing = 0
        try:
            spacing = int(spacing)
            if spacing < 0:
                spacing = 0
            elif spacing > MAX_SAPCING:
                processed_spacing = MAX_SAPCING
            else: 
                processed_spacing = spacing
        except:
            return -1, ERR_SPACING, []
        return 0, ERR_SUCCESS, processed_spacing

    ##################################################################################
    ## valid the digits and spacing
    ## input: self, digits, spacing
    ## output: result, error message, processed_digits, processed spacing
    ##################################################################################
    def valid_params(self, digits, spacing):
        result,errmsg,processed_digits = self.valid_digits(digits)
        if result != 0:
            return result, errmsg, [], []
        result,errmsg,processed_spacing = self.valid_spacing(spacing)
        if result != 0:
            return result, errmsg, [], []
        return 0, ERR_SUCCESS, processed_digits, processed_spacing
        
    
##################################################################################
## Class used to convert the digits to mnist data format. 
## It inherits from the class mnist_data and png_handler.
##################################################################################
class digits_to_png(mnist_data, png_handler):
    ##################################################################################
    ## initialize the variables for itself and its sub classes.
    ## input: self
    ## output: None
    ##################################################################################
    def __init__(self):
        mnist_data.__init__(self)
        png_handler.__init__(self)

    ##################################################################################
    ## format to image data to the as floating point 32bits numpy arrays with a scale ranging from 0 (black) to 1 (white)
    ## input: self, image data
    ## output: processed image data
    ##################################################################################
    def __data_scale(self, image_data):
        float_image_data = image_data.astype('Float32')
        for i in range(float_image_data.shape[0]):
            for j in range(float_image_data.shape[1]):
                if float_image_data[i][j] > 0:
                    float_image_data[i][j] = float_image_data[i][j]/255
                else:
                    float_image_data[i][j] = float_image_data[i][j]
        return float_image_data

    ##################################################################################
    ## deal with all digits and merge the mnist data of them
    ## input: self, digits, spacing
    ## output: processed image data
    ##################################################################################
    def __produce_mnist_data(self, digits, spacing):
        self.get_sample_from_file()
        sample = random.sample(self.sample_map[digits[0]], 1)
        image_data = numpy.reshape(sample, (-1, 28))
        for index in range(1, len(digits)):
            if spacing != 0:
                blank_data = numpy.zeros((self.image_default_height,spacing), dtype = 'int64')
                image_data = numpy.hstack((image_data,blank_data))
            sample = random.sample(self.sample_map[digits[index]], 1)
            file_sample = numpy.reshape(sample, (-1, 28))
            image_data = numpy.hstack((image_data,file_sample))
        return image_data
    
    ##################################################################################
    ## deal with all digits and produce the png image
    ## input: self, digits, spacing
    ## output: error message
    ##################################################################################
    def produce_image(self, digits, spacing, need_valid = 1):
        if need_valid == 1:
            result,errmsg,digits,spacing = params_valid().valid_params(digits,spacing)
            if result != 0:
                return result, errmsg, ''
        image_data = self.__produce_mnist_data(digits, spacing)
        result,errmsg,filepath = self.output_to_image(image_data,image_data.shape[1])
        return result, errmsg, filepath


##################################################################################
## get parameters for the script
## input: None 
## output: digits, spacing
##################################################################################
def get_params():
    p_valid = params_valid()
    digits = []
    while True:
        raw_digits = input("Please input the sequence digits (max digits number: 1000):\nexample:\n0 1 2\n").strip().split(' ')
        result, errmsg, processed_digits = p_valid.valid_digits(raw_digits)
        if result != 0:
            print(errmsg)
            continue
        else:
            digits = processed_digits
            break

    spacing = 0
    while True:
        raw_spacing = input("Please input the spacing between digits (0~200):\n").strip()
        result, errmsg, processed_spacing = p_valid.valid_spacing(raw_spacing)
        if result != 0:
            print(errmsg)
            continue
        else:
            spacing = processed_spacing
            break
    
    print('digits',digits)
    print('spacing', spacing)
    return digits,spacing

##################################################################################
## tests specifies lots of input
## input: None
## output: digits, spacing
##################################################################################
def test_0():
    digits = ['a','b','c']
    spacing = 100
    return digits,spacing

def test_1():
    digits = [3,5,0,'a','b','c',1]
    spacing = 'a'
    return digits,spacing
    
def test_2():
    digits = [1,2,3]
    spacing = -10
    return digits,spacing

def test_3():
    digits = [1,2,3]
    spacing = MAX_SAPCING+1
    return digits,spacing

def test_4():
    digits = [1]
    spacing = 50
    return digits,spacing

def test_5():
    digits = [1,4,6,8,1,3,4,0,9,2,5,1,2,3,4,5,6,8]
    spacing = 50
    return digits,spacing

def test_6():
    digits = [1,4,6,8,1,3,4,0,9,2,5,1,2,3,4,5,6,8]
    spacing = 50
    return digits,spacing

def test_7():
    digits = numpy.random.randint(0,10, MAX_DIGIT_NUM)
    spacing = 50
    return digits,spacing

def test_8():
    digits = numpy.random.randint(0,10, MAX_DIGIT_NUM+1)
    spacing = 50
    return digits,spacing

##################################################################################
## store all the tests
##################################################################################
test_map = [
        test_0(),
        test_1(),
        test_2(),
        test_3(),
        test_4(),
        test_5(),
        test_6(),
        test_7(),
        test_8(),
        ]

##################################################################################
## store all the result
##################################################################################
test_result_map = [
        ERR_DIGIT_NUM,
        ERR_SPACING,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_PRODUCT_IMAGE_SUCCESS,
        ERR_DIGIT_NUM,
        ]

##################################################################################
## run all the tests, and print results of the tests
## input: None
## output: None
##################################################################################
def run_tests():
    p_valid = params_valid()
    d_to_mn = digits_to_png()
    for index in range(len(test_map)):
        digits,spacing = test_map[index]
        result,errmsg,filepath = d_to_mn.produce_image(digits,spacing)
        if test_result_map[index] != errmsg:
            print('Test ', index, ' failed!!')
            print('Expected result is:', test_result_map[index])
            print('Real result is:', errmsg)
        else:
            print('Test ', index, ' succussed!!')

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        run_tests()
    else:
        digits,spacing = get_params()
        d_to_mn = digits_to_png()
        result,errmsg,filepath = d_to_mn.produce_image(digits, spacing, 0)
        print('result:', errmsg)
        print('filepath:', filepath)
