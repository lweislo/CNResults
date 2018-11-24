Attribute VB_Name = "Module6"
Sub a018_UCIResults_v1():

Dim s_name As String
Dim myval As String
Dim mycol As Range
'Check that there are three sheets (Sheet1,2,3) for results macro
Call InsertWorksheets

'Is this really a UCI worksheet?
Call TestUCI
'Let's move the data to Sheet1

Sheets("Results").Select

'Find the last row of results
With ActiveSheet

        If WorksheetFunction.CountA(Cells) > 0 Then
            LastRow = Cells.Find(what:="*", after:=[A1], _
            SearchOrder:=xlByRows, _
            SearchDirection:=xlPrevious).Row
        End If

'Change the case for all caps results
For Each C In Range("F1:F" & LastRow).Cells
    C.Value = Application.WorksheetFunction.Proper(C.Value)
Next C
For Each C In Range("C1:C" & LastRow).Cells
    C.Value = Application.WorksheetFunction.Proper(C.Value)
Next C

Dim tb As ListObject
'assumes Table is the first one on the ActiveSheet
        Set tb = ActiveSheet.ListObjects(1)
        tb.ListColumns("Country").Select

        Call Module1.countriesshort

'Fill in the DNFs etc in the Rank column

For i = 1 To LastRow
    If IsEmpty(tb.DataBodyRange.Cells(i, tb.ListColumns("Rank").Index)) = True Then
        tb.DataBodyRange.Cells(i, tb.ListColumns("Rank").Index) = tb.DataBodyRange.Cells(i, tb.ListColumns("IRM").Index)
    End If
Next i
'Get rid of the lapped riders' info in times colum

For i = 1 To LastRow
   If tb.DataBodyRange.Cells(i, tb.ListColumns("Result").Index) Like "*LAP*" Then
        tb.DataBodyRange.Cells(i, tb.ListColumns("Result").Index) = ""
   End If
Next i
End With


'Finally move the results data to a new Sheet 1

    Dim sheet As Worksheet
    Dim results As Worksheet

    With ActiveWorkbook

    Set s_one = Worksheets("Sheet1")
    Set results = Worksheets("Results")
    
    For i = 1 To LastRow
       s_one.Cells(i, 1).Value = results.Cells(i, 1).Value
       s_one.Cells(i, 2).Value = results.Cells(i, 4).Value & " " & results.Cells(i, 3).Value & " " & _
       results.Cells(i, 5).Value & " " & results.Cells(i, 6).Value
       s_one.Cells(i, 3).Value = results.Cells(i, 11).Value
    Next i
    
    Sheets("Sheet1").Select
    If Cells(1, 1) Like "Rank" Then
        MsgBox "Deleting header row"
        Rows("1:1").Select
        Selection.Delete Shift:=xlUp
    End If
    End With

'Call Module1.TableResults


End Sub


Sub InsertWorksheets()
    Dim worksh As Integer
    Dim worksheetexists As Boolean
    worksh = Application.Sheets.Count
    worksheetexists = False
    
    'Debug.Print worksh
    With ActiveWorkbook
    
    For i = 1 To 3
    
        For x = 1 To worksh
            If Worksheets(x).Name = "Sheet" & i Then
            'MsgBox "Sheet" & i
            worksheetexists = True
            'Debug.Print worksheetexists
            Exit For
            End If
        Next x
        If worksheetexists = False Then
            'Debug.Print "transformed exists"
            Worksheets.Add after:=Worksheets(Worksheets.Count)
            ActiveSheet.Name = "Sheet" & i
        End If
    Next i

    End With
End Sub
        
Sub TestUCI():

    Dim worksh As Integer
    Dim worksheetexists As Boolean
    worksh = Application.Sheets.Count
    worksheetexists = False
    
    With ActiveWorkbook

        For x = 1 To worksh
            If Worksheets(x).Name = "Results" Then
            MsgBox "UCI results file detected. Processing."
            worksheetexists = True
            'MsgBox "WorkSheet Exists"
            Exit For
            End If
        Next x
        If worksheetexists = False Then
            MsgBox "This does not appear to be a UCI results file"
        End If
    End With
End Sub

