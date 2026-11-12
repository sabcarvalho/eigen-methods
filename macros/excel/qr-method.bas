Attribute VB_Name = "Módulo1"
Sub Gerar()
    Dim dimensao As Integer
    dimensao = Worksheets("Plan1").Range("B3").Value
    Range("A5:AA37").Select
    Selection.Delete
    For i = 6 To dimensao + 5 Step 1
        For j = 1 To dimensao Step 1
            Worksheets("Plan1").Cells(i, j).Interior.Color = RGB(204, 204, 204)
            Worksheets("Plan1").Cells(i, j).Borders.LineStyle = xlDouble
        Next
    Next
End Sub
Sub autovetor(ByRef matA() As Double, ByVal dimensao As Integer, ByVal d As Integer, ByVal erro As Double, ByVal multiplicidade As Integer)
    Dim i As Integer, j As Integer, k As Integer
    Dim max As Double, aux As Double
    Dim cont As Integer
    Dim resultado() As Double
    Dim vet() As Double
    ReDim resultado(1 To dimensao, 1 To dimensao)
    ReDim vet(1 To dimensao, 1 To 1)
    For k = 1 To dimensao Step 1 'começo do pivotamento
        If Abs(matA(k, k)) < 0.000001 Then 'se a entrada do pivo for 0, analisa as outras entradas da coluna
            For d1 = k + 1 To dimensao
                If Abs(matA(d1, k)) > Abs(matA(k, k)) Then 'se for 0, continuar analisando
                    For c = 1 To dimensao Step 1
                        aux = matA(k, c)
                        matA(k, c) = matA(d1, c)
                        matA(d1, c) = aux
                    Next c
                Exit For
                End If
            Next d1
        End If
        For e = k + 1 To dimensao Step 1
            If matA(k, k) <> 0 Then
                m = matA(e, k) / matA(k, k)
            'para cada linha será achado um multiplicador para zerar as entradas abaixo do pivo
            matA(e, k) = 0
            For f = k + 1 To dimensao Step 1 'o resto da linha tambem sofrerá alteracoes
                matA(e, f) = matA(e, f) - m * matA(k, f)
            Next f
            End If
        Next e
    Next k
    aux_mult = 0
    If Abs(matA(dimensao, dimensao)) < 0.000001 And multiplicidade = 0 Then 'se a última linha da matriz for toda nula, a última entrada do autovetor será 1
        vet(dimensao, 1) = 1
    Else
        vet(dimensao, 1) = 0 'senão, será 0
    End If
    For e = (dimensao - 1) To 1 Step -1 'a resolução começará de baixo pra cima, a partir da penultima linha
        aux = 0 'o auxiliar é zerado a cada iteração
        For f = dimensao To e Step -1
            'as entradas da matriz original vao sendo multiplicadas pelos valores do autovetor que já foram encontrados e sendo subtraidos, pois o resultado do sistema é nulo
            aux = aux - vet(f, 1) * matA(e, f)
        Next f
        If Abs(matA(e, e)) < 0.00001 Then 'o coeficiente da entrada analisada passa dividindo o resultado
            aux = 1
        Else
            aux = aux / matA(e, e)
        End If
        vet(e, 1) = aux
        If multiplicidade > 0 And aux_mult < multiplicidade Then
            vet(dimensao - aux_mult, 1) = 0
            aux_mult = aux_mult + 1
        End If
    Next e
    j = dimensao + 1 + d
    aux = 0
    For i = 1 To dimensao
        aux = aux + vet(i, 1) * vet(i, 1)
    Next i
    aux = Sqr(aux)
    For i = 7 + dimensao To dimensao * 2 + 6
        Worksheets("Plan1").Cells(i, j).Value = vet(i - 6 - dimensao, 1) / aux
    Next
End Sub
Sub Calcular()
    Dim coss As Double
    Dim seno As Double
    Dim max As Double
    Dim dimensao, i, j, k, p, q, c, d, multiplicidade As Integer
    Dim cont As Integer
    dimensao = Worksheets("Plan1").Range("B3").Value
    erro = Worksheets("Plan1").Range("B4").Value
    Dim a() As Double
    Dim matU() As Double
    Dim matQ() As Double
    Dim matR() As Double
    Dim resultado() As Double
    Dim transU() As Double
    Dim autovalores() As Double
    ReDim a(1 To dimensao, 1 To dimensao)
    ReDim matU(1 To dimensao, 1 To dimensao)
    ReDim matQ(1 To dimensao, 1 To dimensao)
    ReDim matR(1 To dimensao, 1 To dimensao)
    ReDim resultado(1 To dimensao, 1 To dimensao)
    ReDim transU(1 To dimensao, 1 To dimensao)
    ReDim autovalores(1 To dimensao, 1 To 1)
    For i = 6 To dimensao + 5 Step 1
        For j = 1 To dimensao Step 1
            a(i - 5, j) = Worksheets("Plan1").Cells(i, j).Value
        Next
    Next
    cont = 1
    Do
        cont = cont + 1
        For c = 1 To dimensao Step 1
            For d = 1 To dimensao Step 1
                matR(c, d) = a(c, d)
            Next
        Next
        'identidade
        For i = 1 To dimensao Step 1
            For j = 1 To dimensao Step 1
                If i = j Then
                    matQ(i, j) = 1
                Else
                    matQ(i, j) = 0
                End If
            Next
        Next
        For i = 2 To dimensao Step 1
            j = 1
            Do While j < i
                If matR(i, j) <> 0 Then
                    p = j
                    q = i
                    'identidade
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            If c = d Then
                                matU(c, d) = 1
                            Else
                                matU(c, d) = 0
                            End If
                        Next
                    Next
                    coss = matR(p, p) / Sqr(matR(p, p) ^ 2 + matR(q, p) ^ 2)
                    seno = matR(q, p) / Sqr(matR(p, p) ^ 2 + matR(q, p) ^ 2)
                    matU(p, p) = coss
                    matU(q, q) = coss
                    matU(q, p) = -seno
                    matU(p, q) = seno
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            resultado(c, d) = 0
                        Next
                    Next
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            For k = 1 To dimensao Step 1
                                resultado(c, d) = resultado(c, d) + matU(c, k) * matR(k, d)
                            Next
                        Next
                    Next
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            matR(c, d) = resultado(c, d)
                        Next
                    Next
                                    
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            resultado(c, d) = 0
                        Next
                    Next
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            transU(c, d) = matU(d, c)
                        Next
                    Next
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            For k = 1 To dimensao Step 1
                                resultado(c, d) = resultado(c, d) + matQ(c, k) * transU(k, d)
                            Next
                        Next
                    Next
                    For c = 1 To dimensao Step 1
                        For d = 1 To dimensao Step 1
                            matQ(c, d) = resultado(c, d)
                        Next
                    Next
                End If
            j = j + 1
            Loop
        Next
        For i = 1 To dimensao Step 1
            For j = 1 To dimensao Step 1
                resultado(i, j) = 0
            Next
        Next
        For i = 1 To dimensao Step 1
            For j = 1 To dimensao Step 1
                For k = 1 To dimensao Step 1
                    resultado(i, j) = resultado(i, j) + matR(i, k) * matQ(k, j)
                Next
            Next
        Next
        For c = 1 To dimensao Step 1
            For d = 1 To dimensao Step 1
                a(c, d) = resultado(c, d)
            Next
        Next
        max = 0
        For i = 2 To dimensao Step 1
            j = 1
            Do While j < i
                If Abs(a(i, j)) > max Then
                    max = Abs(a(i, j))
                End If
                j = j + 1
            Loop
        Next
    Loop While max > erro And cont < 1000 'se os autovetores estiverem nulos, talvez aumentando as iterações ajude
    espaco = dimensao + 2
    Worksheets("Plan1").Cells(6, espaco).Value = "Erro Calculado: "
    Worksheets("Plan1").Cells(6, espaco + 1).Value = max
    Worksheets("Plan1").Cells(7, espaco).Value = "Número de Iterações: "
    Worksheets("Plan1").Cells(7, espaco + 1).Value = cont
    Worksheets("Plan1").Cells(dimensao + 6, espaco).Value = "Autovetores: "
    cont = 0
    aux = 6 + dimensao
    For i = 7 + dimensao To dimensao * 2 + 6 Step 1
        For j = 1 To dimensao Step 1
            Worksheets("Plan1").Cells(i, j).Value = a(i - 6 - dimensao, j)
            If i - j = aux Then
            cont = cont + 1
            Worksheets("Plan1").Cells(i, j).Interior.Color = RGB(204, 204, 204)
            autovalores(cont, 1) = Worksheets("Plan1").Cells(i, j).Value
            End If
        Next
    Next
    For d = 1 To dimensao
        For i = 6 To dimensao + 5 Step 1
            For j = 1 To dimensao Step 1
                matR(i - 5, j) = Worksheets("Plan1").Cells(i, j).Value
            Next
        Next
        For i = 1 To dimensao Step 1
            matR(i, i) = matR(i, i) - autovalores(d, 1)
        Next i
        multiplicidade = 0
        If d > 1 Then
            For j = 1 To d - 1 Step 1
                If Abs(autovalores(d, 1) - autovalores(j, 1)) < 0.000001 Then
                    multiplicidade = multiplicidade + 1
                End If
            Next j
        End If
        autovetor matR, dimensao, d, erro, multiplicidade
    Next d
End Sub

