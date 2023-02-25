import re
import abc
#from Backend.src.parser_generic import MedicalDocParser

class MedicalDocParser(metaclass=abc.ABCMeta):
    def __init__(self, text):
        self.text = text

    @abc.abstractmethod
    def parse(self):
        pass


class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)

    def parse(self):
        return {
            'Patient_name': self.get_field('Patient_name'),
            'Patient_address': self.get_field('Patient_address'),
            'Medicines': self.get_field('Medicines'),
            'Directions': self.get_field('Directions'),
            'Refills': self.get_field('Refills')
        }



    def get_field(self, field_name):
        pattern_dict = {
            'Patient_name': {'pattern': 'Name:(.*)Date', 'flags': 0},
            'Patient_address': {'pattern': 'Address:(.*)\n', 'flags': 0},
            'Medicines': {'pattern': 'Address[^\n]*(.*)Directions', 'flags': re.DOTALL},
            'Directions': {'pattern': 'Directions:(.*)Refill', 'flags': re.DOTALL},
            'Refills': {'pattern': 'Refill:(.*)times', 'flags': 0},
        }


        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object['pattern'], self.text, flags=pattern_object['flags'])
            if len(matches) > 0:
                return matches[0].strip()

if __name__ == '__main__':
    document_text = '''
Dr John Smith, M.D
2 Non-Important Street,
New York, Phone (000)-111-2222
Name: Maria Sharapova Date: 5/11/2022
Address: 9 tennis court, new Russia, DC

Prednisone 20 mg
Lialda 2.4 gram
Directions:
Prednisone, Taper 5 mg every 3 days,
Finish in 2.5 weeks -
Lialda - take 2 pill everyday for 1 month
Refill: 3 times
'''
    pp = PrescriptionParser(document_text)
    print(pp.parse())
