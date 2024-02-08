import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from datetime import datetime
import calendar


incomes  = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses","Saving"]
currency = "USD"
page_title = "Income and Expense Tracker"
page_icon = "💰"
layout  = "centered"



# ----------------------------------------

st.set_page_config(page_title=page_title, 
                   page_icon=page_icon,
                   layout= layout )

st.title(page_title + " " + page_icon)




#------------------------------ DROP DOWN VALUES FOR SELECTING THE PERIOD----
years  = [datetime.today().year, datetime.today().year + 1]
months  = list(calendar.month_name[1:])

## --------HIDE STREAMLIT STYLE--------------
hide_st_style = """
            <style>
            #MainmMenu {visibiity: hidden;}
            footer {visibility:hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


## -----------NAVIGATION MENU------
selected  = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualisation"],
    icons=["pencil-fill", "bar-chart-fill"],
    orientation="horizontal"
    
)


#----------------Input and save period
if selected == "Data Entry":
    

    st.header(f"Data entry in {currency}")
    with st.form("entry_form",clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")
        
        
        "_ _ _"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        
        
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i",step=10, key= expense)
                
            
        with st.expander("Comment"):
            comment  = st.text_area("", placeholder="Enter a Comment here......")
            
        "_ _ _"
        
        submitted  = st.form_submit_button("Save Data")
        if submitted :
            period  = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            income  = {income : st.session_state[income] for income in incomes}
            expenses  = {expense:st.session_state[expense] for expense in expenses}
            
            #  TODO: iNSERT VALUES TO DATABASE
            st.write(f"incomes: {incomes}")
            st.write(f"expenses: {expenses}")
            st.success("Data Saved!")

    
    
        
#-----------PLOT PERIODS-----------
if selected == "Data Visualisation":
    
    st.header("Data Visualisation")
    with st.form("saved_periods"):
        # TODO: Get Periods from database
        period  = st.selectbox("Select Period :", ["2022_March"])
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # TODO: gET the data from database
            comment = "Some comment"
            incomes  = {'Salary':1500, 'Blog':50,'Other Income':10}
            expenses = {'Rent':600,'Utilities':200,'Groceries':300,
                        'Car':100,'Other Expenses':50,'Saving':10}
            
            ## create metrics
            total_income  = sum(incomes.values())
            total_expense  = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget",f"{remaining_budget} {currency}")
            st.text(f"Comment: {comment}")
            
            
            ## create SANKEY CHART

            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())

            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)

            # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
            
        
        
     
    
    
    



