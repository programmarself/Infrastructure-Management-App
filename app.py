import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load Data
assets = pd.read_csv('data/assets.csv')
maintenance = pd.read_csv('data/maintenance.csv')

# Page Setup
st.set_page_config(page_title='Infrastructure Management System', layout='wide')
st.title('Smart Infrastructure Management System')

# Sidebar Navigation
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Assets", "Maintenance", "Reports", "About"])

# Dashboard Page
if page == "Dashboard":
    st.header('Dashboard Overview')

    # Summary Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assets", len(assets))
    col2.metric("Total Maintenance", len(maintenance))
    col3.metric("Average Maintenance Cost", f"${maintenance['Cost'].mean():.2f}")

    # Condition Pie Chart
    fig_pie = px.pie(assets, names='Condition', title='Asset Conditions')
    st.plotly_chart(fig_pie, use_container_width=True)

    # Maintenance Cost Over Time
    maintenance['Date'] = pd.to_datetime(maintenance['Date'])
    fig_line = px.line(maintenance, x='Date', y='Cost', title='Maintenance Costs Over Time', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# Assets Page
elif page == "Assets":
    st.header('Asset Management')

    st.write('### All Assets')
    st.dataframe(assets)

    st.write('### Filter Assets')
    asset_type = st.selectbox('Select Asset Type', options=['All'] + assets['Type'].unique().tolist())
    if asset_type != 'All':
        filtered_assets = assets[assets['Type'] == asset_type]
    else:
        filtered_assets = assets
    st.dataframe(filtered_assets)

# Maintenance Page
elif page == "Maintenance":
    st.header('Maintenance Management')

    st.write('### Maintenance Records')
    st.dataframe(maintenance)

    st.write('### Add New Maintenance Record')
    with st.form("maintenance_form"):
        asset_id = st.selectbox('Select Asset', assets['AssetID'])
        date = st.date_input('Maintenance Date')
        description = st.text_input('Description')
        cost = st.number_input('Cost', min_value=0)
        submitted = st.form_submit_button('Add Record')

        if submitted:
            new_record = {'MaintenanceID': len(maintenance)+1, 'AssetID': asset_id, 'Date': date, 'Description': description, 'Cost': cost}
            maintenance = maintenance.append(new_record, ignore_index=True)
            maintenance.to_csv('data/maintenance.csv', index=False)
            st.success('Record Added Successfully!')

# Reports Page
elif page == "Reports":
    st.header('Reports and Visualizations')

    fig_bar = px.bar(assets, x='AssetName', y=assets['AssetName'].map(lambda x: maintenance[maintenance['AssetID'] == assets[assets['AssetName'] == x]['AssetID'].values[0]]['Cost'].sum()), labels={'y': 'Total Maintenance Cost'}, title='Maintenance Cost per Asset')
    st.plotly_chart(fig_bar, use_container_width=True)

# About Page
elif page == "About":
    st.header('About This Project')
    st.write('This Smart Infrastructure Management System helps in tracking assets, managing maintenance, and visualizing asset performance.')
    st.write('Developed by: Irfan Ullah Khan')
    st.write('Contact: [GitHub](https://github.com/programmarself) | [LinkedIn](https://www.linkedin.com/in/iukhan/)')
    # Footer with Font Awesome icons
st.markdown("---")
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
    .social-icons {
        margin: 20px 0;
    }
    .social-icons a {
        margin: 0 10px;
        color: #1E90FF;
        font-size: 24px;
        transition: color 0.3s, transform 0.3s;
        text-decoration: none;
    }
    .social-icons a:hover {
        color: #FF4500;
        transform: scale(1.2);
    }
    .footer {
        text-align: center;
        font-size: 16px;
        padding: 20px 0;
    }
    </style>
    <div class="footer">
      <p>&copy; 2025 Smart Infrastructure Management System | All rights reserved</p>
      <p><strong>Developed with ❤️ by Irfan Ullah Khan</strong></p>
      <div class="social-icons">
        <a href="https://github.com/programmarself" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
        <a href="https://www.linkedin.com/in/iukhan/" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
        <a href="https://programmarself.github.io/My_Portfolio/" target="_blank" title="Portfolio"><i class="fas fa-briefcase"></i></a>
        <a href="mailto:programmarself@gmail.com" title="Email"><i class="fas fa-envelope"></i></a>
      </div>
    </div>
""", unsafe_allow_html=True)
