class Clubbing:
    """
        This class shall  be used to combining the data from the column occupation_type.
    """

    def club(self,X):
        """
                Method Name: club
                Description: This method clubs the data from the column occupation_type.
                On Failure: Raise Exception
        """
        try:
            Occupation = {
                'Managers': 'Occup1',
                'Realty agents': 'Occup1',
                'Drivers': 'Occup2',
                'Accountants': 'Occup2',
                'IT staff': 'Occup2',
                'Private service staff': 'Occup2',
                'High skill tech staff': 'Occup2',
                'HR staff': 'Occup3',
                'Core staff': 'Occup3',
                'Laborers': 'Occup4',
                'Security staff': 'Occup4',
                'Sales staff': 'Occup4',
                'Not Available': 'Occup5',
                'Secretaries': 'Occup5',
                'Medicine staff': 'Occup5',
                'Waiters/barmen staff': 'Occup5',
                'Cleaning staff': 'Occup6',
                'Cooking staff': 'Occup6',
                'Low-skill Laborers': 'Occup6'
            }
            X['OCCUPATION_TYPE'] = X['OCCUPATION_TYPE'].replace(Occupation)
            return X
        except Exception as e:
          raise Exception()

