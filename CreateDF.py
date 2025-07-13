
def create_DF():
    import pandas as pd
    import numpy as np
    DIST_VA = pd.read_excel('data/2324_VA_DIST_DETAILS.xlsx', sheet_name=1,index_col=0)
    DIST_GRAD_RATE = pd.read_excel('data/2024_DISTRICT_GRAD_RATE.xlsx', sheet_name=1,index_col=0)
    DIST_RACE_DIS = pd.read_excel('data/2324_DIST_RACE_DIS.xlsx', sheet_name=1,index_col=0)
    DIST_DETAIL = pd.read_excel('data/2024_District_Details.xlsx', sheet_name=1,index_col=0)
    DIST_ACHEIVE = pd.read_excel('data/23-24_Achievement_District.xlsx', sheet_name=1,index_col=0)
    DIST_SPEND = pd.read_excel('data/2324_DISTRICT_SPEND_PER_PUPIL.xlsx', sheet_name=1,index_col=0)
    DIST_INCOME_TAX = pd.read_excel('data/22_TAX_INCOME.xlsx', sheet_name=1,index_col=3)
    DIST_PROPERTY_TAX = pd.read_excel('data/DIST_PROPERTY_TAX.xlsx', sheet_name=1,index_col=2)
    # Clean Distric Value Added DF
    DIST_VA = DIST_VA.drop(columns = 'Watermark')
    # Clean Distric Graduation Rate DF
    DIST_GRAD_RATE = DIST_GRAD_RATE.drop(columns=['District Name','County','Region','Watermark'])
    # Clean Distric Detail DF
    import pandas as pd
    import numpy as np
    
    def transform_district_data(df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
    
        if data.index.name:
            district_id_col = data.index.name
        else:
            # Fallback if the index is not named
            district_id_col = 'District ID'
            data.index.name = district_id_col
    
        data.reset_index(inplace=True)
    
        data['Enrollment'] = pd.to_numeric(data['Enrollment'], errors='coerce')
        data['Attendance Rate'] = pd.to_numeric(data['Attendance Rate'], errors='coerce')
    
        pivoted_data = data.pivot_table(
            index=district_id_col,
            columns='Student Group',
            values='Enrollment'
        ).fillna(0).astype(int)
    
        all_students_df = data[data['Student Group'] == 'All Students'].set_index(district_id_col)
        total_attendance_map = all_students_df['Attendance Rate']
    
        if 'All Students' in pivoted_data.columns:
            pivoted_data.rename(columns={'All Students': 'Total Students'}, inplace=True)
    
        pivoted_data['Total Attendance Percent'] = pivoted_data.index.map(total_attendance_map)
    
        if 'Total Students' in pivoted_data.columns:
            student_group_cols = [col for col in pivoted_data.columns if col not in ['Total Students', 'Total Attendance Percent']]
            final_order = ['Total Students', 'Total Attendance Percent'] + student_group_cols
            pivoted_data = pivoted_data[final_order]
    
        return pivoted_data.reset_index()
    DIST_DETAIL = transform_district_data(DIST_DETAIL)
    DIST_DETAIL.set_index('District IRN', inplace=True)
    DIST_ACHEIVE = DIST_ACHEIVE.drop(columns=['District Name','County','Region','Watermark','Maximum District Performance Index Score 2023-2024'])
    # Clean District Spend
    DIST_SPEND = DIST_SPEND.drop(columns=['District Name','County','Region','Watermark','State-Level Expenditures per Equivalent Pupil','State-Level Expenditures per Equivalent Pupil - Federal Funds','State-Level Expenditures per Equivalent Pupil - State and Local Funds'])
    
    DIST_INCOME_TAX.drop(columns=['COUNTY','SCHOOL DISTRICT','PUN','SCHOOL DISTRICT NUMBER'],inplace=True)
    DIST_PROPERTY_TAX.drop(columns=['County','School District Number','PUN','School District Name','Rank'],inplace=True)
    # Join Dataframes
    combined_df = pd.merge(DIST_VA,DIST_GRAD_RATE, on='District IRN')
    combined_df = pd.merge(combined_df,DIST_DETAIL, on='District IRN')
    combined_df = pd.merge(combined_df,DIST_ACHEIVE, on='District IRN')
    combined_df = pd.merge(combined_df,DIST_SPEND, on='District IRN')
    combined_df = pd.merge(combined_df,DIST_INCOME_TAX, on='District IRN')
    combined_df = pd.merge(combined_df,DIST_PROPERTY_TAX, on='District IRN')
    combined_df.drop(48975,inplace=True)
    
    #convert Numbers
    combined_df['Overall Composite'] = combined_df['Overall Composite'].astype(float)
    combined_df['Overall Effect Size'] = combined_df['Overall Effect Size'].astype(float)
    combined_df['Graduation Rate Component Percent (Weighted Graduation Rate)'] = combined_df['Graduation Rate Component Percent (Weighted Graduation Rate)'].astype(float)
    combined_df['Four Year Graduation Rate - Class of 2023'] = combined_df['Four Year Graduation Rate - Class of 2023'].astype(float)
    combined_df['Four Year Graduation Rate Numerator - Class of 2023'] = combined_df['Four Year Graduation Rate Numerator - Class of 2023'].astype(float)
    combined_df['Four Year Graduation Rate Denominator - Class of 2023'] = combined_df['Four Year Graduation Rate Denominator - Class of 2023'].astype(float)
    combined_df['Five Year Graduation Rate - Class of 2022'] = combined_df['Five Year Graduation Rate - Class of 2022'].astype(float)
    combined_df['Five Year Graduation Rate Numerator - Class of 2022'] = combined_df['Five Year Graduation Rate Numerator - Class of 2022'].astype(float)
    combined_df['Five Year Graduation Rate Denominator - Class of 2022'] = combined_df['Five Year Graduation Rate Denominator - Class of 2022'].astype(float)
    #convert Money and Stars
    combined_df['Expenditures per Equivalent Pupil'] = combined_df['Expenditures per Equivalent Pupil'].str.replace(r'[$,€£]', '', regex=True).str.replace(',', '').astype(float)
    combined_df['Expenditures per Equivalent Pupil - Federal Funds'] = combined_df['Expenditures per Equivalent Pupil - Federal Funds'].str.replace(r'[$,€£]', '', regex=True).str.replace(',', '').astype(float)
    combined_df['Expenditures per Equivalent Pupil - State and Local Funds'] = combined_df['Expenditures per Equivalent Pupil - State and Local Funds'].str.replace(r'[$,€£]', '', regex=True).str.replace(',', '').astype(float)
    
    #Stars
    
    combined_df['Progress Component Star Rating'] = combined_df['Progress Component Star Rating'].str.replace(' Stars','', regex=True).str.replace(' Star','',regex=True).astype(int)
    combined_df['Graduation Rate Component Rating'] = combined_df['Graduation Rate Component Rating'].str.replace(' Stars','', regex=True).str.replace(' Star','',regex=True).astype(int)
    combined_df['Achievement Component Star Rating'] = combined_df['Achievement Component Star Rating'].str.replace(' Stars','', regex=True).str.replace(' Star','',regex=True).astype(int)
    
    
    # Effective Property Tax Rate
    combined_df['Effective Property Tax Rate'] = (combined_df['Real Property Taxes Charged'] / combined_df['Real Property Taxable Value (a)']) * 100
    
    # Effective Income Tax Rate
    combined_df['Effective Income Tax Rate'] = (combined_df['TOTAL OHIO INCOME TAX LIABILITY'] / combined_df['TOTAL OHIO INCOME TAX BASE']) * 100
    
    # Total Local Tax Burden (Overall Local Effective Rate)
    combined_df['Total Local Tax Burden'] = (combined_df['Total Taxes'] / combined_df['Total Value']) * 100
    
    # Per Capita Income Tax Liability
    combined_df['Per Capita Income Tax Liability'] = combined_df['TOTAL OHIO INCOME TAX LIABILITY'] / combined_df['NUMBER OF RETURNS']
    
    # Student to Taxpayer Ratio
    combined_df['Student to Taxpayer Ratio'] = combined_df['Total Students'] / combined_df['NUMBER OF RETURNS']
    
    # Funding Source Percentages
    combined_df['Federal Funding Percentage'] = (combined_df['Expenditures per Equivalent Pupil - Federal Funds'] / combined_df['Expenditures per Equivalent Pupil']) * 100
    combined_df['State and Local Funding Percentage'] = (combined_df['Expenditures per Equivalent Pupil - State and Local Funds'] / combined_df['Expenditures per Equivalent Pupil']) * 100
    
    # Student Demographic Percentages
    combined_df['Percent of Economically Disadvantaged Students'] = (combined_df['Economic Disadvantage'] / combined_df['Total Students']) * 100
    combined_df['Percent of Students with Disabilities'] = (combined_df['Students with Disabilities'] / combined_df['Total Students']) * 100
    combined_df['Percent of American Indian or Alaskan Native'] = (combined_df['American Indian or Alaskan Native'] / combined_df['Total Students']) * 100
    combined_df['Percent of Asian or Pacific Islander'] = (combined_df['Asian or Pacific Islander'] / combined_df['Total Students']) * 100
    combined_df['Percent of Black, Non-Hispanic'] = (combined_df['Black, Non-Hispanic'] / combined_df['Total Students']) * 100
    combined_df['Percent of English Learner'] = (combined_df['English Learner'] / combined_df['Total Students']) * 100
    combined_df['Percent of Hispanic'] = (combined_df['Hispanic'] / combined_df['Total Students']) * 100
    combined_df['Percent of Migrant'] = (combined_df['Migrant'] / combined_df['Total Students']) * 100
    combined_df['Percent of Multiracial'] = (combined_df['Multiracial'] / combined_df['Total Students']) * 100
    combined_df['Percent of White, Non-Hispanic'] = (combined_df['White, Non-Hispanic'] / combined_df['Total Students']) * 100
    
    columns_to_drop = [
        'Four Year Graduation Rate Numerator - Class of 2023',
        'Four Year Graduation Rate Denominator - Class of 2023',
        'Five Year Graduation Rate Numerator - Class of 2022',
        'Five Year Graduation Rate Denominator - Class of 2022',
    
        'Real Property Taxes Charged',
        'Public Utility Tangible Property Taxable Value',
        'Public Utility Tangible Property Taxes Levied',
        'Total Value',
        'Total Taxes',
        'Real Property',
        'Public Utility Tangible Property',
        'Amount',
        'TOTAL FEDERAL ADJUSTED GROSS INCOME',
        'TOTAL OHIO ADJUSTED GROSS INCOME',
        'TOTAL OHIO BUISNESS INCOME DEDUCTION',
        'TOTAL OHIO INCOME TAX BASE',
        'TOTAL OHIO INCOME TAX LIABILITY',
    
        'ADJUSTED GROSS INCOME RANK',
        'MEDIAN FEDERAL ADJUSTED GROSS INCOME RANK',
        'AVERAGE OHIO ADJUSTED GROSS INCOME RANK',
        'MEDIAN OHIO ADJUSTED GROSS INCOME RANK',
    
        'NUMBER OF PERSONAL EXEMPTIONS',
    'NUMBER OF SENIOR CITIZEN CREDITS'
    ]

    combined_df.drop(columns=columns_to_drop,inplace=True)
    return combined_df