REM  *****  BASIC  *****
'Global resultado(dimensao, dimensao) as Object
Sub Gerar
	BasicLibraries.LoadLibrary("LibreMacro")
	dim dimensao as Integer
	dimensao = Cell("Planilha1", "B3").Value
	Apagar()
	for i = 6 to dimensao + 5 step 1
		for j = 1 to dimensao step 1
			Cell("Planilha1", REF(i,j)).CellBackColor =  RGB(204, 204, 204)
		next
	next
	Bordas(dimensao)
End Sub

Sub Calcular
	BasicLibraries.LoadLibrary("LibreMacro")
	dim coss as Double
	dim seno as Double
	dim max as Double
	dim dimensao, i, j, k, p, q, c,d, multiplicidade as Integer
	dim cont as Integer
	dimensao = Cell("Planilha1", "B3").Value
	dim a(dimensao, dimensao) as Double
	dim matU(dimensao,dimensao) as Double
	dim matQ(dimensao, dimensao) as Double
	dim matR(dimensao, dimensao) as Double
	dim resultado(dimensao,dimensao) as Double
	dim transU(dimensao, dimensao) as Double
	dim autovalores(dimensao, 1) as Double
	erro = Cell("Planilha1", "B4").Value
	for i = 6 to dimensao + 5 step 1
		for j = 1 to dimensao step 1
			a(i-5, j) = Cell("Planilha1", REF(i,j)).Value
		next
	next
	cont = 1
	Do
		cont = cont+1	
		for c = 1 to dimensao step 1
			for d = 1 to dimensao step 1
				matR(c,d)=a(c,d)
			next
		next
		'identidade
		for i = 1 to dimensao step 1
			for j = 1 to dimensao step 1
				If i = j Then
					matQ(i,j) = 1
				Else
					matQ(i,j) = 0
				End If
			next
		next
		for i = 2 to dimensao step 1
			j = 1
			Do while j < i
				If matR(i, j) <> 0 Then
					p = j
					q = i
					'identidade
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							If c = d Then
								matU(c,d) = 1
							Else
								matU(c,d) = 0
							End If
						next
					next
					coss = matR(p,p)/Sqr(matR(p,p)^2 + matR(q, p)^2)
					seno = matR(q,p)/Sqr(matR(p,p)^2 + matR(q, p)^2)
					matU(p,p) = coss
					matU(q,q) = coss
					matU(q,p) = -seno
					matU(p,q) = seno
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							resultado(c,d)=0
						next
					next
					for c = 1 to dimensao step 1
						for d=1 to dimensao step 1
							for k=1 to dimensao step 1
								resultado(c,d) = resultado(c,d) + matU(c,k)* matR(k,d)
							next
						next
					next
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							matR(c,d)=resultado(c,d)
						next
					next
									
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							resultado(c,d)=0
						next
					next
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							transU(c,d)=matU(d,c)
						next
					next
					for c = 1 to dimensao step 1
						for d=1 to dimensao step 1
							for k=1 to dimensao step 1
								resultado(c,d) = resultado(c,d) + matQ(c,k)*transU(k,d)
							next
						next
					next
					for c = 1 to dimensao step 1
						for d = 1 to dimensao step 1
							matQ(c,d)=resultado(c,d)
						next
					next
				End If		
			j = j+1
			Loop
		next
		for i = 1 to dimensao step 1
			for j = 1 to dimensao step 1
				resultado(i,j)=0
			next
		next
		for i = 1 to dimensao step 1
			for j=1 to dimensao step 1
				for k=1 to dimensao step 1
					resultado(i,j) = resultado(i,j) + matR(i,k)* matQ(k,j)
				next
			next
		next
		for c = 1 to dimensao step 1
			for d = 1 to dimensao step 1
				a(c,d)=resultado(c,d)
			next
		next
		max = 0
		for i = 2 to dimensao step 1
			j = 1
			Do While j<i
				If 	Abs(a(i, j))>max Then
					max = Abs(a(i, j))
				End If	
				j = j+1
			Loop
		next
	Loop While max>erro And cont<1000 'se os autovetores estiverem nulos, talvez aumentando as iterações ajude
	espaco = dimensao +2
	Cell("Planilha1", REF(6,espaco)).String = "Erro Calculado: "
	Cell("Planilha1", REF(6,espaco+1)).Value = max
	Cell("Planilha1", REF(7,espaco)).String = "Número de Iterações: "
	Cell("Planilha1", REF(7,espaco+1)).Value = cont 
	Cell("Planilha1", REF(dimensao+6,espaco)).String = "Autovetores: "
	cont = 0
	aux = 6+dimensao
	for i = 7 + dimensao to dimensao*2 + 6 step 1
		for j = 1 to dimensao step 1
			Cell("Planilha1", REF(i,j)).Value = a(i-6-dimensao, j)
			if i - j = aux Then
			cont = cont+1
			Cell("Planilha1", REF(i,j)).CellBackColor =  RGB(204, 204, 204)	
			autovalores(cont, 1) = Cell("Planilha1", REF(i,j)).Value		
			End if
		next
	next	
	for d = 1 to dimensao
	 	for i = 6 to dimensao + 5 step 1
			for j = 1 to dimensao step 1
				matR(i-5, j) = Cell("Planilha1", REF(i,j)).Value
			next
		next
		for i = 1 to dimensao step 1
			matR(i,i) = matR(i,i) - autovalores(d, 1)
		next i
		multiplicidade = 0
		If d>1 then
			For j = 1 to d-1 step 1
				If Abs(autovalores(d,1) - autovalores(j,1))<0.000001 then
					multiplicidade = multiplicidade+1
				End If
			next j
		End If
		autovetor(matR, dimensao, d, erro, multiplicidade)
	next d
End Sub

Sub autovetor(matA as Double, dimensao as Integer, d as Integer, erro as Integer, multiplicidade as Integer)
    Dim vet(dimensao, 1) As Double
    Dim k, d1, c, e, f As Integer
    Dim m, aux, aux_mult As Double
    For k = 1 To dimensao step 1 'começo do pivotamento
        If Abs(matA(k,k))<0.000001 Then 'se a entrada do pivo for 0, analisa as outras entradas da coluna
        	For d1 = k+1 to dimensao
                If Abs(matA(d1,k)) > Abs(matA(k,k)) Then 'se for 0, continuar analisando
                    For c = 1 To dimensao step 1
                    	aux = matA(k,c)
                    	matA(k,c) = matA(d1,c)
                   		matA(d1,c) = aux
                	Next c
                Exit for
                end if
            next d1
        End If
        For e = k+1 To dimensao step 1
        	If matA(k,k)<>0 then
        		m = matA(e,k)/matA(k,k)
            'para cada linha será achado um multiplicador para zerar as entradas abaixo do pivo
            matA(e,k) = 0
            For f = k+1 To dimensao step 1 'o resto da linha tambem sofrerá alteracoes
                matA(e,f) = matA(e,f) - m*matA(k,f)
            Next f
            
            end if
        Next e
    Next k
    aux_mult = 0
    If Abs(matA(dimensao,dimensao))<0.000001 AND multiplicidade = 0 Then 'se a última linha da matriz for toda nula, a última entrada do autovetor será 1
        vet(dimensao,1)=1
    Else
        vet(dimensao,1)=0 'senão, será 0
    End If
    For e = dimensao-1 To 1 Step -1 'a resolução começará de baixo pra cima, a partir da penultima linha
        aux = 0 'o auxiliar é zerado a cada iteração
        For f = dimensao To e-1 Step -1
            'as entradas da matriz original vao sendo multiplicadas pelos valores do autovetor que já foram encontrados e sendo subtraidos, pois o resultado do sistema é nulo
            aux = aux - vet(f,1)*matA(e,f)
        Next f
        If Abs(matA(e,e))<0.00001 Then 'o coeficiente da entrada analisada passa dividindo o resultado
            aux = 1
        Else
            aux = aux/matA(e,e)
        End If
        vet(e,1)=aux
        If multiplicidade>0 AND aux_mult<multiplicidade then
        	vet(dimensao-aux_mult,1) = 0
        	aux_mult = aux_mult + 1
        End If
    Next e
	j = dimensao+1 +d
	aux = 0
	for i= 1 to dimensao
		aux = aux + vet(i,1)*vet(i,1)
	next i
	aux = Sqr(aux)
	for i= 7 + dimensao to dimensao*2 +6
		If(aux<>0) then
		Cell("Planilha1", REF(i,j)).Value = vet(i-6-dimensao,1)/aux
		End If
	next
End Sub


