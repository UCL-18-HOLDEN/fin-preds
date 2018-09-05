def get_rolled_window(columns,ts_length,df):
    """
    need to name ts column 'series'
    need to name date as 'date'
    date is at the zero time step

    Also note that the columns must be of the appropriate window size
    """

    new_df=[]

    for idx,row in enumerate(df['date']):

        if idx>=(TS_LENGTH-1):
            new_row = []
            for i in range(TS_LENGTH):
                new_row.append(df['series'].loc[(idx-i)])
            new_row.append(df['date'].loc[idx])

            new_df.append(new_row)


    rolled_window = pd.DataFrame(new_df,columns=columns)
    return rolled_window





def get_prices(companies):

    """
    note we can change date range as desired
    close price is used as open price is not tracked in european markets (wharton)


    """
    date_rng = pd.date_range(start='11-11-2014',end='6-7-2018', freq='W')

    df = pd.DataFrame()

    for dt in date_rng:
        df1 = companies[companies['datadate']==dt]
        while df1.empty:
            dt = dt-pd.DateOffset(days=1)
            df1 = companies[companies['datadate']==dt]
        df = df.append(df1)


    df.reset_index(drop=True,inplace=True)
    df = df.rename(columns={'prccd':'previous_week_close'})

    df['week_close'] = df['previous_week_close'].shift(-1)
    df['weekly_ret'] = df['week_close'] - df['previous_week_close']
    df['weekly_pct'] = 1.0*df['weekly_ret']/df['previous_week_close']

    return df
