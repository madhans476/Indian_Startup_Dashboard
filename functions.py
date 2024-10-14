import streamlit as st 
import altair as alt


color1 = 'Orange'
color2 = 'Blue'

def capitalize_column_names(data):
    data.columns = [col[0].upper() + col[1:] if col else col for col in data.columns]


def bar_line_and_df(data, subtype, year_wise):
    data = data.reset_index()
    s = 'Counts'
    if year_wise == 'Amount Funded':
        s = 'Total ₹ (Cr)'
    data.columns = ['Year', s]
    
    if subtype == 'Barplot':
        # fig, ax = plot_style(subtype)
        # axis = sns.barplot(x=data['Year'], y=data[s],color="Orange", ax=ax)

        # # Add labels to the bars
        # for container in axis.containers:
        #     axis.bar_label(container, fmt='%d', padding=3, color='white')
        # ax.tick_params(axis='x', colors='white')  
        # ax.tick_params(axis='y', colors='white')
        # ax.set_title(f'{s} Over Years', fontsize=16)
        # ax.set_xlabel('Year', fontsize=12)
        # ax.set_ylabel(f'{s}', fontsize=12)
        # st.pyplot(fig)
        # download_plot(fig, year_wise, f"{year_wise}_{subtype}.png")

        bars = alt.Chart(data).mark_bar(size=35).encode(
            x=alt.X('Year:N', title='Year'),
            y=alt.Y(f'{s}:Q', title=s),
            color=alt.value(color1),
            tooltip=[
            alt.Tooltip("Year", title="Year: "),
            alt.Tooltip(s, title=f'{s}: ', format='.0f'),
        ],
        ).properties(
            height = 350,
        ).configure_axis(
            labelAngle= 0,
            labelFontSize=12,
        )

        # Hover interaction
        highlight = alt.selection_single(on='mouseover', empty='none')

        # Chart with hover effect
        bars = bars.encode(
            color=alt.condition(highlight, alt.value(color2), alt.value(color1)),
            size=alt.condition(highlight, alt.value(55), alt.value(35))  # Enlarges on hover
        ).add_selection(
            highlight
        )

        st.altair_chart(bars, use_container_width=True)

    elif subtype == 'Lineplot':
        #! Static plot
        # fig, ax = plot_style(subtype)
        # sns.lineplot(x=data['Year'], y=data[s], marker='o', color=color1, linewidth=2.5)
        # ax.set_title(f'{s} Over Years', fontsize=16)
        # ax.set_xlabel('Year', fontsize=12)
        # ax.set_ylabel(f'{s}', fontsize=12)

        # st.pyplot(fig)
        # download_plot(fig, year_wise, f"{year_wise}_{subtype}.png")
        hover = alt.selection_single(on='mouseover', nearest=True, empty='none', fields=['Year'])
    
        line_chart = alt.Chart(data).mark_line(color=color1, point=True).encode(
            x=alt.X('Year:O', title='Year', axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f'{s}:Q', title=f'{s}',),
            tooltip=[
            alt.Tooltip("Year", title="Year: "),
            alt.Tooltip(s, title=f'{s}: ', format='.0f'),
        ]
        ).properties(
            width=600,
            height=400
        )

        # Add hover effect for color change
        highlight_points = line_chart.mark_circle(size=100).encode(
            color=alt.condition(hover, alt.value(color2), alt.value(color1)),
            size=alt.condition(hover, alt.value(150), alt.value(100))
        ).add_selection(
            hover
        )

        # Combine line chart and highlighted points
        final_chart = (line_chart + highlight_points).properties(
        ).configure_axis(
            labelColor='white',
            labelAngle=0,
            grid=False
        ).configure_view(
            strokeWidth=0
        ).configure_title(
            color='white',
            fontSize=16
        ).configure()  # Apply background config here

        # Display the chart in Streamlit
        st.altair_chart(final_chart, use_container_width=True)
    else:            
        data['Year'] = data['Year'].astype(str)
        st.write('Data Overview:')
        capitalize_column_names(data)
        st.dataframe(data.style.set_properties(**{
            'background-color': '#262730',
            'border': '1px solid black',
            # 'color': 'black',
            'text-align': 'center'
        }), width = 400)


def Barplot(n,data,x,y, c):
    bh = 68/c
    min_bh = 500/c
    ch = max(n * bh, min_bh)

    base_bar_size = 60/c 
    min_bar_size = 10/c
    bar_size = max(base_bar_size - n * (1.2), min_bar_size)

    if x == 'amount':
        xt = 'Total ₹ (Cr)'
    else: 
        xt = x[0].upper() + x[1:]
    yt = y[0].upper() + y[1:]
    bars = alt.Chart(data).mark_bar(size=bar_size).encode(
        x=alt.X(x, title=x),
        y=alt.Y(y, title=y, sort='-x'),
        color=alt.value(color1),
        tooltip=[alt.Tooltip(x, title=f"{xt}: ", format='.0f'), alt.Tooltip(y, title=f"{yt}: " )]
    ).properties(
        height = ch
    ).configure_axis(
        labelFontSize=12,
    )

    # Hover interaction
    highlight = alt.selection_single(on='mouseover', empty='none')

    # Chart with hover effect
    bars = bars.encode(
        color=alt.condition(highlight, alt.value(color2), alt.value(color1)),
        size=alt.condition(highlight, alt.value(bar_size+(bar_size/4)), alt.value(bar_size))  # Enlarges on hover
    ).add_selection(
        highlight
    )

    # Show chart in Streamlit
    st.altair_chart(bars, use_container_width=True)



def DataFrame(n,data, amount = False):
    if amount == True:
        data.rename(columns={'amount': 'Total ₹ (Cr)'}, inplace=True)
    capitalize_column_names(data)
    st.write('Data Overview:')
    h = n*41
    st.dataframe(data.style.set_properties(**{
            'background-color': '#262730',
            'border': '1px solid black',
            'text-align': 'center'
        }), height = h, width = 450)
