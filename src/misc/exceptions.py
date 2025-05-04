import sys

def error_message_detail(error, error_detail:sys):      ## Function to be called when an exception is called / An error occurs
    _,_,exc_tb = error_detail.exc_info()                ## First 2 outputs are irrelevent. The 3rd output contains all details regarding the error
    file_name = exc_tb.tb_frame.f_code.co_filename      ## Extract File Name

    error_message = f"\n An error has occured in file: {0} \n Line number: {1} \n Error message: {2}".format()
    file_name, exc_tb.tb_lineno, str(error)

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_details)

    def __str__(self):
        return self.error_message
