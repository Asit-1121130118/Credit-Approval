import till_merge
import clubbing
import encoding


class EDA:

    def __init__(self):
        self.input_file_1_loc = 'EDA_DATA/application_record.csv'
        self.input_file_2_loc = 'EDA_DATA/credit_record.csv'

    def EDAPipeline(self):

        edaobj = till_merge.EDA
        clubbingobj = clubbing.Clubbing()
        encodingobj = encoding.Encoding()



        application_file = edaobj.read_file(self.input_file_1_loc)
        credit_file = edaobj.read_file(self.input_file_2_loc)

        cred_df_g, application_clean = edaobj.get_distinct_values(application_file,credit_file)

        merged_data = edaobj.label_data(cred_df_g, application_clean)

        merged_data = clubbingobj.club(merged_data)

        merged_data = encodingobj.encode(merged_data)

        merged_data.to_csv('dData.csv')





        return merged_data



if __name__ == "__main__":
    obj = EDA()
    data = obj.EDAPipeline()
    print(data)
