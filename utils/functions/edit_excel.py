from decouple import config
import pandas as pd
import os
import win32com.client as win32


def edit(subzone_2_present: bool, df_filtered: pd.DataFrame) -> None:

    excel = win32.Dispatch('Excel.Application')

    wb = excel.Workbooks.Open(os.path.abspath(
        f'./storage/{config('FILE_NAME')}'))

    excel.Visible = False

    ws = wb.Sheets(1)

    try:
        for row in range(2, ws.UsedRange.Rows.Count + 1):
            ws.Cells(
                row, 3).Value = df_filtered.at[row - 2, config('EXCEL_SUBZONE_3')]
            ws.Cells(
                row, 4).Value = df_filtered.at[row - 2, config('EXCEL_SUBZONE_4')]
            ws.Cells(
                row, 5).Value = df_filtered.at[row - 2, config('EXCEL_SUBZONE_5')]

        wb.SaveAs(os.path.abspath(
            f'./storage/{config('FILE_NAME')[:-5]}-Actualizado.xlsx'))

        wb.Close(SaveChanges=True)

        excel.Quit()

    except Exception as e:

        wb.SaveAs(os.path.abspath(
            f'./storage/{config('FILE_NAME')[:-5]}-Fallido-{e}.xlsx'))

        wb.Close(SaveChanges=True)

        excel.Quit()
