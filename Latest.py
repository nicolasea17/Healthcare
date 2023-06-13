import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# Define the correct username and password
correct_username = "nea17"
correct_password = "ilovehealthcare"

# Create a Streamlit sidebar
st.sidebar.markdown("## MSBA 350E")
st.sidebar.markdown("## Welcome to Nicolas Araman's Dashboard")

# Add the text above the sign-in information
st.sidebar.markdown("Username: nea17")
st.sidebar.markdown("Password: ilovehealthcare")
st.sidebar.markdown("Enjoy the access while it lasts")

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    # Add input fields for username and password
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Create a login button
    if st.sidebar.button("Login"):
        # Check if the username and password are correct
        if username == correct_username and password == correct_password:
            # Mark the user as logged in
            st.session_state['logged_in'] = True
            # Mark all sections as selected
            st.session_state['selected_pages'] = ["Introduction", "Visualization", "Customize Your Chart"]
        else:
            st.error("Invalid username or password")

# Rest of the code...


# If the user is logged in, show the main app content
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    # Set the main page title to "Cardiovascular Disease"
    st.title("Cardiovascular Disease")

    # Add the image to the main page
    st.image("https://drive.google.com/uc?id=15-s2wCQie90aQ3KRTBHe5uXh89plPBiU")

    # Create a Streamlit sidebar for navigation
    st.sidebar.empty()  # Remove the username and password fields
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    selected_pages = st.sidebar.multiselect(
        "Go to",
        ("Introduction", "Visualization", "Customize Your Chart"),
        default=st.session_state.get('selected_pages', [])
    )

    # Specify the file path
    file_path = "cleaned_cardio.csv"

    # Download the file using requests
    url = "https://drive.google.com/uc?id=1Tnb8EwnHUE4SyqIqyqA9lfZksvtGSpN4"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
    else:
        st.error("Failed to download the dataset file.")

    # Load the CSV file
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Failed to find the dataset file.")

    if "Introduction" in selected_pages:
        st.title("Introduction")
        st.markdown("Cardiovascular disease refers to a group of conditions that affect the heart and blood vessels. It is a broad term that encompasses various disorders, including:")

        # Define the conditions and their definitions
        conditions = {
            "Coronary artery disease (CAD)": "It occurs when the arteries that supply blood to the heart become narrowed or blocked due to the buildup of plaque, a fatty substance. CAD can lead to chest pain (angina), heart attacks, and other heart-related complications.",
            "Hypertension (high blood pressure)": "It is a condition characterized by consistently elevated blood pressure levels. If left untreated, hypertension can strain the heart and blood vessels, increasing the risk of heart disease, stroke, and other cardiovascular problems.",
            "Stroke": "A stroke occurs when the blood supply to the brain is interrupted, either due to a blood clot (ischemic stroke) or a ruptured blood vessel (hemorrhagic stroke). Strokes can cause permanent brain damage and can be life-threatening.",
            "Heart failure": "It is a condition in which the heart cannot pump enough blood to meet the body's needs. Heart failure can result from various underlying causes, such as CAD, high blood pressure, or previous heart damage.",
            "Arrhythmias": "Arrhythmias are irregular heart rhythms that can manifest as a fast, slow, or irregular heartbeat. They can disrupt the normal pumping function of the heart and cause symptoms like palpitations, dizziness, and fainting.",
            "Valvular heart disease": "It refers to conditions affecting the heart valves, which control the flow of blood through the heart chambers. Valvular heart disease can involve valve stenosis (narrowing) or regurgitation (leakage), impairing the heart's ability to pump blood efficiently."
        }

        # Add expandable sections for each condition
        for condition, definition in conditions.items():
            with st.expander(condition):
                st.write(definition)
    if "Visualization" in selected_pages:
        st.title("Visualization")
        # Perform visualizations using the loaded dataset
        if st.button("Dissect BMI - Weight and Height", key="visualization_button"):
            # Toggle between weight and height vs cardio and BMI vs cardio
            if "Weight_Height" in st.session_state:
                # Remove existing visualization
                del st.session_state['Weight_Height']
            else:
                # Add weight and height vs cardio scatter plot
                fig = px.scatter(data, x="Weight", y="Height", color="Cardio", title="Weight and Height vs. Cardio")
                st.plotly_chart(fig, use_container_width=True)
                st.session_state['Weight_Height'] = True

        # Add BMI vs cardio violin chart
        fig = px.violin(data, y="BMI", x="Cardio", box=True, color="Cardio", title="BMI vs. Cardio")
        st.plotly_chart(fig, use_container_width=True)

        # Add Blood Pressure Category vs Cardio interactive bar chart
        fig = px.bar(data, x="Blood_Pressure_Category", color="Cardio", title="Blood Pressure Category vs. Cardio")
        fig.update_layout(barmode='group', xaxis={'categoryorder':'array', 'categoryarray':['elevated', 'high', 'normal']})
        fig.update_xaxes(title="Blood Pressure Category")
        fig.update_yaxes(title="Count")
        st.plotly_chart(fig, use_container_width=True)

        # Create a cross-tabulation between Active and Cardio
        crosstab = pd.crosstab(data['Active'], data['Cardio'])

        # Convert the crosstab to a percentage representation
        crosstab_percent = crosstab.div(crosstab.sum(1), axis=0)

        # Reset index for plotting
        crosstab_percent = crosstab_percent.reset_index()

        # Create a stacked bar chart
        fig = px.bar(
            crosstab_percent,
            x='Active',
            y=[False, True],
            title="Active Status vs. Cardio",
            barmode="stack",
            labels={"x": "Active", "y": "Percentage"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        # Update the legend and axis labels
        fig.update_layout(legend_title="Cardio", xaxis_title="Active", yaxis_title="Percentage")
        st.plotly_chart(fig, use_container_width=True)

        # Convert the numerical gender values to corresponding labels
        data['Gender'] = data['Gender'].map({1: 'Male', 2: 'Female'})

        # Create a grouped bar chart
        fig = px.histogram(
            data_frame=data,
            x='Gender',
            color='Cardio',
            barmode='group',
            category_orders={'Gender': ['Female', 'Male']},
            title="Gender vs. Cardio"
        )

        # Update the legend and axis labels
        fig.update_layout(
            legend_title="Cardio",
            xaxis_title="Gender",
            yaxis_title="Count",
            bargap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)

        # Create a violin plot
        fig = px.violin(data, y="Age", x="Cardio",
                        box=True, points="all",
                        color="Cardio", violinmode="overlay",
                        labels={"Cardio": "Cardiovascular Disease",
                                "Age": "Age"},
                        category_orders={"Cardio": [False, True]},
                        title="Distribution of Age by Cardiovascular Disease")

        # Update layout and axis labels
        fig.update_layout(
            xaxis_title="Cardiovascular Disease",
            yaxis_title="Age",
            legend_title="Cardio",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

            # Create a DataFrame with counts for each Cholesterol and Cardio category
    counts = data.groupby(['Cholesterol', 'Cardio']).size().reset_index(name='Count')

    # Define the Cholesterol categories and their order
    cholesterol_categories = ['Normal', 'Well_Above_Normal', 'Above_Normal']

        # Add a visualization for glucose levels vs cardio
    fig = px.histogram(data, x="Glucose", color="Cardio", barmode="group", title="Glucose Levels vs. Cardio")
    fig.update_layout(xaxis_title="Glucose Level", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

    # Create a function to switch between chart types
    def toggle_chart_type():
        if reveal_truth:
            # Create a stacked bar chart
            fig = px.bar(counts, x='Cholesterol', y='Count', color='Cardio', barmode='stack',
                         labels={'Cholesterol': 'Cholesterol', 'Count': 'Count', 'Cardio': 'Cardiovascular Disease'},
                         category_orders={'Cholesterol': cholesterol_categories},
                         title='Cholesterol vs Cardio Stacked Bar Chart')

            fig.update_layout(
                legend_title='Cardio',
                xaxis_title='Cholesterol',
                yaxis_title='Count'
            )
        else:
            # Create a radar chart
            fig = go.Figure()

            for cardio_value in [True, False]:
                values = counts[counts['Cardio'] == cardio_value]['Count'].tolist()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=cholesterol_categories,
                    fill='toself',
                    name='Cardio ' + str(cardio_value)
                ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True
                    )
                ),
                showlegend=True,
                title='Cholesterol vs Cardio Radar Chart'
            )

        st.plotly_chart(fig, use_container_width=True)

    # Add a button for the toggle
    reveal_truth = st.button("Reveal the Truth")

    # Call the toggle_chart_type function
    toggle_chart_type()

    if "Customize Your Chart" in selected_pages:
        st.title("Customize Your Chart")
        # Get the list of available variables for customization
        variables = data.columns.tolist()

        # Create selection dropdowns for x and y variables
        x_variable = st.selectbox("Select the X-axis variable", variables)
        y_variable = st.selectbox("Select the Y-axis variable", variables)

        # Check if the chosen variables are categorical or numerical
        x_is_categorical = data[x_variable].dtype == 'object'
        y_is_categorical = data[y_variable].dtype == 'object'

        # Generate the customized chart based on the variable types
        if x_is_categorical and y_is_categorical:
            chart_types = ["Bar Chart"]
        elif x_is_categorical and not y_is_categorical:
            chart_types = ["Bar Chart", "Box Plot"]
        elif not x_is_categorical and y_is_categorical:
            chart_types = ["Violin Plot"]
        else:
            chart_types = ["Scatter Plot"]

        # Select the chart type
        chart_type = st.selectbox("Select the chart type", chart_types)

        # Generate the chart based on the selected options
        if chart_type == "Bar Chart":
            fig = px.bar(data, x=x_variable, y=y_variable, color=x_variable, title=f"{x_variable} vs. {y_variable}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Box Plot":
            fig = px.box(data, x=x_variable, y=y_variable, color=x_variable, title=f"{x_variable} vs. {y_variable}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Violin Plot":
            fig = px.violin(data, x=x_variable, y=y_variable, color=x_variable, title=f"{x_variable} vs. {y_variable}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Scatter Plot":
            fig = px.scatter(data, x=x_variable, y=y_variable, color=x_variable, title=f"{x_variable} vs. {y_variable}")
            st.plotly_chart(fig, use_container_width=True)
