import streamlit as st
import pandas as pd
import requests

st.title("Welcome to the Elections SMS App")






def send(index_no, phone, password):
    website = 'https://election.njace.edu.gh/'
    sender_id = 'NJACOLLEGE'
    url = 'https://mysms.pingafrik.com/api/sms/send'
    payload = {
        'key': 'dUFdr',
        'secret': 'coLfbB0Zxi0Q',
        'contacts': phone,
        'sender_id': f'{sender_id}',
        'message': f"VOTING DETAILS\nIndex No: {index_no}\nPassword: {password}\n Portal: {website}"
    }

    response = requests.post(url, data=payload)
    print(response.text)

st.write('___')

# Step 1: Define your database model using SQLAlchemy's ORM
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class Voters(Base):
    __tablename__ = 'voters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    index_no = Column(String)
    phone = Column(String)
    level = Column(String)
    password = Column(String)
    # Add more columns as needed

# Step 2: Create the database and its tables
engine = create_engine('sqlite:///instance/send_sms.db')
Base.metadata.create_all(engine)

# Step 3: Read data from the Excel file into a DataFrame
excel_file_path = './voter_register.xlsx'
df = pd.read_excel(excel_file_path)

# Step 4: Insert the data from the DataFrame into the database
Session = sessionmaker(bind=engine)
session = Session()
for index, row in df.iterrows():
    existing_entry = session.query(Voters).filter_by(index_no=row['Index No']).first()
    if existing_entry:
        pass
    else:
        new_entry = Voters(name=row['Names'], index_no=row['Index No'], level=row['Level'], phone=row['Phone'], password=row['Password'])
        session.add(new_entry)
        print(f'Entry for index {row["Index No"]} added')
session.commit()
session.close()


search  = st.text_input('Search', placeholder='Search by index number')
st.write('___')


if search:
    # search database for the index number

    users = session.query(Voters).filter(Voters.index_no.contains(search)).all()
    if users:
        col1, col2, col3, col4, col5 = st.columns(5)

        for user in users:
            with col1:
                st.write(user.name)
               

            with col2:
                st.write(user.index_no)
               
            
            with col3:
                st.write(f"0{user.phone}")
               
            
            with col4:
                if st.button('Send', key=user.index_no, type='secondary'):
                    send(user.index_no, user.phone, user.password)
                    st.success('SMS sent')
            with col5:
                st.write(user.password)
    else:
        st.write('No results found')






