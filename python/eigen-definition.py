#calculo do det(A-Lambda*I)
from numpy import identity, array
import numpy as np
import sympy as sp
from sympy import Symbol, nroots, eye
from sympy.matrices import eye, Matrix


def determinante(dim, mat):
  matAux = identity(dim, dtype='object')
  if dim == 2:
    p = mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
  else:
    p = 0
    for k in range(0, dim):
      a = 0 #linha da matriz auxiliar
      b = 0 #coluna da matriz auxiliar
      for c in range(1, dim): #para o calculo do det uso a primeira linha da matriz
        for d in range(0, dim):
          if d != k:
            matAux[a][b] = mat[c][d]
            b = b + 1
        a = a + 1
        b = 0
      p = p + (-1)**k*mat[0][k]*determinante(dim-1, matAux)
  return p

#calculo dos autovetores

def autovetor(d, mat_aux, matrizp, dim): #indice autovetor = d
  vet = np.zeros(dim)
  for k in range(dim-1):
    if mat_aux[k][k] == 0:
      #se o valor do pivotamento é zero, é preciso trocar as linhas
        for d1 in range(k+1, dim): #o d1 percorre todos os valores abaixo do pivo
            if mat_aux[d1][k] != 0:
              #se encontrou algum valor diferente de zero, a linha sera trocada
                mat_aux[[k,d1]] = mat_aux[[d1,k]] # troca as linhas k e d1
                break
    for e in range(k+1, dim):
      if mat_aux[k][k] != 0:
      #se o pivo é diferente de zero, acharemos o fator de multiplicacao
        m = mat_aux[e][k]/mat_aux[k][k]
        mat_aux[e][k] = 0 # valor abaixo do pivo eh zerado
        for f in range(k+1, dim):
          #aqui, as linhas abaixo do pivo sao subtraidas pelos valores da linha do pivo*m
          mat_aux[e][f] = mat_aux[e][f] - m*mat_aux[k][f]
  #terminado o loop, o ultimo elemento da ultima linha eh analizado
  if mat_aux[dim-1][dim-1].simplify()!=0:
    matrizp[dim-1, d]=0 #se for 0, o autovetor tera a ultima entrada zerada
    #a matriz P sera construida, com o autovetor associado ao lambda_d na posicao d
  else:
    matrizp[dim-1, d]=1 #se for 1, o autovetor tera a ultima entrada igual a 1
  #a resolução começará de baixo pra cima, a partir da penultima linha
  for e in range(dim-2, -1, -1):
    aux=0 #o auxiliar é zerado a cada iteração
    for f in range(dim-1, e,-1):
      #as entradas da matriz original vao sendo multiplicadas pelos valores do autovetor
      #que já foram encontrados e sendo subtraidos, pois o resultado do sistema é nulo
      aux = aux + matrizp[f,d]*mat_aux[e][f]
    if mat_aux[e][e] != 0:
      aux = aux/mat_aux[e][e] #o coeficiente da entrada analisada passa dividindo o resultado
      matrizp[e,d]=-aux.simplify()
    else:
      matrizp[e,d] = 1

#funcao main
def main(a):
  dim = np.shape(a)[0]
  mat_aux = a.astype(object)
  lamb = Symbol('x') #variavel iniciada
  for i in range(0, dim):
    for j in range(0, dim):
      if i==j: mat_aux[i][i] -=lamb #colocando lambda na diagonal
      print(mat_aux[i,j], end=' ')
    print('')
  #a funcao determinante eh chamada com a matriz aux com lamb da diagonal como variavel
  polinomio = determinante(dim,mat_aux).factor()
  #a funcao factor fatora o polinomio resultante do calculo do determiante
  print(f'Polinomio: {polinomio}')
  #o dominio do polinomio eh restrito aos reais, nao calculando os imaginarios
  polinomio = polinomio.as_poly(domain='QQ')
  #o polinomio eh resolvido com a funcao all_roots e as raizes vao para o vetor sol
  sol = polinomio.all_roots()
  print(f'Raízes: {sol}')
  matrizp = eye(dim)
  for d in range(0, dim):
    #para cada autovalor encontrado, a matriz A original vai ser copiada e
    #o lambda sera substituido com o valor do indice d do vetor sol
    print(f'Para o autovalor {sol[d]}: ')
    for i in range(0, dim):
      for j in range(0, dim):
        mat_aux[i][j] = a[i][j]
        if i == j:
          mat_aux[i][j] = a[i][j] - sol[d]
        print(mat_aux[i][j], end=' ')
      print('')
    #funcao autovetor eh chamada com a matriz (a-lamb_d)
    autovetor(d, mat_aux, matrizp, dim)
  #terminado o loop, a matrizp foi construida, com todos os autovetores de A
  print('Matriz P: ')
  for i in range(0, dim):
    for j in range(0, dim):
      print(matrizp[i,j], end=' ')
    print('')
  #aqui temos a matriz inversa de P para calcularmos a matriz diagonal
  inversa = matrizp.inv()
  print(f'Matriz inversa de P: ')
  for i in range(0, dim):
    for j in range(0, dim):
      print(inversa[i,j], end=' ')
    print('')
  d = inversa*a*matrizp
  print(f'Matriz diagonal D = P**-1 * A * P: ')
  for i in range(0, dim):
    for j in range(0, dim):
      if not d[i,j].is_rational:
        d[i,j] = d[i,j].evalf()
      print(d[i,j].simplify(), end=' ')
    print('')
if __name__ == "__main__":
   a=array([[3, -1, 0], [-1, 2, -1], [0, -1, 3]])
   main(a)