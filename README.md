# sudoku
Intial code
def input_sudoku():
    sudomat = []
    for j in range(9):
        row = []
        print('Enter the values of row' + repr(j))
        for i in range(9):
            # x = int(input( ))
            x = i
            row.append(x)
        sudomat[j:] = [row]
        print('row' + str(j), row)
    return sudomat


def print_sudoku(sudomat):
    for m in range(9):
        y = sudomat[m]
        if m == 3 or m == 6:
            print()
        print()
        for z in range(9):
            print(y[z], end=' ')
            if z == 2 or z == 5:
                print('', end=' ')
    return None

def scan_horizontal(x, y, sudomat):
    for m in range(9):
        horizontal = sudomat[m]
        if y == m:
            return horizontal

def scan_vertical(x, y, sudomat):
    transposed = []
    for i in range(9):
        transposed.append([row[i] for row in sudomat])
    for m in range(9):
        vertical = transposed[m]
        if x == m:
            return vertical


def scan_square(x, y, sudomat):
    transposed = []
    square = []
    if x <= 2:
        for i in range(3):
            transposed.append([row[i] for row in sudomat])
        if y <= 2:
            for elements in transposed:
                for j in range(3):
                    square.append(elements[j])

        if y > 2 and y <= 5:
            for elements in transposed:
                for j in range(3, 6):
                    square.append(elements[j])

        if y > 5:
            for elements in transposed:
                for j in range(6, 9):
                    square.append(elements[j])

    if x > 2 and x <= 5:
        for i in range(3, 6):
            transposed.append([row[i] for row in sudomat])
        if y <= 2:
            for elements in transposed:
                for j in range(3):
                    square.append(elements[j])

        if y > 2 and y <= 5:
            for elements in transposed:
                for j in range(3, 6):
                    square.append(elements[j])

        if y > 5:
            for elements in transposed:
                for j in range(6, 9):
                    square.append(elements[j])

    if x > 5:
        for i in range(6, 9):
            transposed.append([row[i] for row in sudomat])
        if y <= 2:
            for elements in transposed:
                for j in range(3):
                    square.append(elements[j])

        if y > 2 and y <= 5:
            for elements in transposed:
                for j in range(3, 6):
                    square.append(elements[j])

        if y > 5:
            for elements in transposed:
                for j in range(6, 9):
                    square.append(elements[j])
    return square


def sudoku_update(x, y, upt_mat, upt_value):
    transposed = []
    for i in range(9):
        transposed.append([row[i] for row in upt_mat])

    transposedx = []
    for i in range(9):
        transposedx.append([row[i] for row in transposed])

    zzz = transposedx[y]

    if zzz[x] == 0:
        zzz[x] = upt_value
    return transposedx


def sudoku_solve_all(x, y, sudomat):
    xxx = sudomat[x]
    if xxx[y] == 0:
        a = set(scan_vertical(x, y, sudomat))
        b = set(scan_horizontal(x, y, sudomat))
        c = set(scan_square(x, y, sudomat))
        d = (a | b | c)
        e = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} - d

        # #print ('e for', x,y, 'is', e)
        f = len(e)
        if f == 1:
            for g in e:
                return (sudoku_update(x, y, sudomat, g))

    return sudomat


def sudosolv_horizontal(x, y, sudomat):
 xxx = sudomat[x]
 a = []
 o = 0
 z = {1,2,3,4,5,6,7,8,9}
 if xxx[y] == 0:
    if y <= 2:
        m = 0
        for t in range(3):
           if xxx[t] == 0:
               m = m + 1
        if m == 1:
           for i in range(3, 9):
              if xxx[i] == 0:
                a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                o = o + 1
        for n in a:
         z = n & z
        u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                  set(scan_square(y, x, sudomat))))
        k = len(u)
        if k == 1:
            for v in u:
                return sudoku_update(y,x , sudomat, v)


    if y > 2 and y <= 5:
        m = 0
        for t in range(3,6):
            if xxx[t] == 0:
                m = m + 1
        if m == 1:
            for i in (0, 1, 2, 6, 7, 8):
                if xxx[i] == 0:
                    a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                    o = o + 1
        for n in a:
         z = n & z
        u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                    set(scan_square(y, x, sudomat))))
        k = len(u)
        if k == 1:
           for v in u:
              return sudoku_update(y,x,sudomat,v)


    if y > 5:
         m=0
         for t in range(6, 9):
            if xxx[t] == 0:
              m = m + 1
         if m == 1:
            for i in range(6):
                if xxx[i] == 0:
                    a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                    o = o + 1
         for n in a:
            z = n & z
         u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                    set(scan_square(y, x, sudomat))))
         k = len(u)
         if k == 1:
            for v in u:
                return sudoku_update(y,x, sudomat, v)
 return sudomat


def sudosolve_intellect_lookup (x,y,sudomat):
    xxx = sudomat[x]
    #print (' the scanned row is', xxx)
    a = []
    o = 0
    z = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    #print ('the value of xxx[y] is', xxx[y])
    if xxx[y] == 0:
        #print ('the value of scanned value is blank- solving')
        if y <= 2:
            m = 0
            for t in range(3):
                if xxx[t] == 0:
                    m = m + 1
            if m == 1:
                for i in range(3, 9):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
            if m > 1 :
                for i in range (3):
                    if xxx[i] == 0 and i != y:
                        a[o:] = [(set(scan_vertical(i,x,sudomat)) | set(scan_square(i,x,sudomat))) ]
                        o = o + 1
                for i in range(3, 9):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
                #print ('the value of a is', a)
            for n in a:
                z = n & z
            #print ( 'z value is',z )
            u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                  set(scan_square(y, x, sudomat))))
            k = len(u)
            if k == 1:
                for v in u:
                  return sudoku_update(y,x , sudomat, v)


        if  y > 2 and y <= 5:
            m = 0
            for t in range(3,6):
                if xxx[t] == 0:
                    m = m + 1
            if m == 1:
                for i in (0,1,2,6,7,8):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
            if m > 1 :
                for i in range (3,6):
                    if xxx[i] == 0 and i != y:
                        a[o:] = [(set(scan_vertical(i,x,sudomat)) | set(scan_square(i,x,sudomat))) ]
                        o = o + 1
                for i in (0,1,2,6,7,8):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
                #print ('the value of a is', a)
            for n in a:
                z = n & z
            #print ( 'z value is',z )
            u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                  set(scan_square(y, x, sudomat))))
            k = len(u)
            if k == 1:
                for v in u:
                  return sudoku_update(y,x , sudomat, v)



        if y > 5:
            m = 0
            for t in range(6,9):
                if xxx[t] == 0:
                    m = m + 1
            if m == 1:
                for i in range(6):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
            if m > 1 :
                for i in range (6,9):
                    if xxx[i] == 0 and i != y:
                        a[o:] = [(set(scan_vertical(i,x,sudomat)) | set(scan_square(i,x,sudomat))) ]
                        o = o + 1
                for i in range(6):
                    if xxx[i] == 0:
                        a[o:] = [(set(scan_vertical(i, x, sudomat)) | set(scan_square(i, x, sudomat)))]
                        o = o + 1
                #print ('the value of a is', a)
            for n in a:
                z = n & z
            #print ( 'z value is',z )
            u = z - ((set(scan_vertical(y, x, sudomat))) | (set(scan_horizontal(y, x, sudomat))) | (
                  set(scan_square(y, x, sudomat))))
            k = len(u)
            if k == 1:
                for v in u:
                  return sudoku_update(y,x , sudomat, v)
    return sudomat



def sudosolv_vertical (x,y,sudomat):
  transposed = []
  for w in range(9):
        transposed.append([row[w] for row in sudomat])

  sudomatx = sudosolve_intellect_lookup(x,y,transposed)

  transposedx =[]

  for q in range (9):
      transposedx.append ([rowx[q] for rowx in sudomatx])

  return transposedx


def sudo_num_unsolved (sudomat):
    m =0
    for xxx in sudomat:
          for i in range (9):
             if xxx[i] == 0:
                  m=m+1
    return print ("\nthe number of unresolved items is ", m)


def validate_sudoku (sudomat):
 identifier = 0
 for i in range (9):
     x = scan_horizontal(0,i,sudomat)
     m =0
     for k in x:
         m =0
         for o in range (9):
          if k != 0 and k == x[o]:
              m = m+1
         if m > 1 :
             break
     if m > 1 :
         break
 if m > 1:
     identifier = 1

 #print('the value of identifier is', identifier)

 for j in range (9):
     y = scan_vertical(j,0,sudomat)
     n =0
     for l in y:
         n =0
         for p in range (9):
          if l != 0 and k == y[p]:
              n = n+1
         if n > 1 :
             break
     if n > 1 :
         break
 if n > 1:
     identifier = 2

 #print('the value of identifier is', identifier)

 c =0
 d =[]
 for a in range (0,9,3):
     for b in range (0,9,3):
               d[c:] = [scan_square(a,b,sudomat )]
               c = c+1
 for i in range (9):
     x = scan_horizontal(0,i,d)
     m =0
     for k in x:
         m =0
         for o in range (9):
          if k != 0 and k == x[o]:
              m = m+1
         if m > 1 :
             break
     if m > 1 :
         break
 if m > 1:
     identifier = 3

 #print('the value of identifier is', identifier)


 for aa in range (9):
     o = 0
     a = []
     uuu = sudomat[aa]
     z = {1,2,3,4,5,6,7,8,9}
     #print ('\nmat is', uuu )
     for bb in range (9):
         if uuu[bb] == 0:
             a[o:] = [(set(scan_vertical(bb, aa, sudomat)) | set(scan_square(bb, aa, sudomat)) | set (scan_horizontal(bb,aa,sudomat)))]
             o = o + 1
     for n in a:
         z = n & z
     #print ( 'the value of z before', z )
     z = z -  set (scan_horizontal(bb,aa,sudomat))
     #print ('the scan horizontal set value is', set (scan_horizontal(bb,aa,sudomat)))
     if len(z) != 0:
         identifier = 4
         break

 #print('the value of identifier is', identifier)

 transposed = []
 for w in range(9):
     transposed.append([row[w] for row in sudomat])
 #print_sudoku(transposed)

 for aa in range (9):
     o = 0
     a = []
     uuu = transposed[aa]
     z = {1,2,3,4,5,6,7,8,9}
     #print ('\nmat is', uuu )
     for bb in range (9):
         if uuu[bb] == 0:
             a[o:] = [(set(scan_vertical(bb, aa, transposed)) | set(scan_square(bb, aa, transposed)) | set (scan_horizontal(bb,aa,transposed)))]
             o = o + 1
     #print ( 'the vaule of a', a)
     for n in a:
         z = n & z
     #print ( 'the value of z before', z )
     z = z -  set (scan_horizontal(bb,aa,transposed))
     #print ('the scan horizontal set value is', set (scan_horizontal(bb,aa,transposed)))
     if len (z) != 0:
         identifier = 5
         break

 #print ('the value of identifier is', identifier)



 for xx in range (0,9,3):
     for yy in range (0,9,3):
         f = 0
         ee= []
         zz = {0,1,2,3,4,5,6,7,8,9}
         for cc in range (3):
             for dd in range (3):
                 if sudomat[xx + cc][yy + dd] == 0:
                     ee[f:] = [set(scan_vertical((yy + dd), (xx + cc), sudomat)) | set(
                         scan_horizontal((yy + dd), (xx + cc), sudomat)) | set(
                         scan_square((yy + dd), (xx + cc), sudomat))]
                     f = f +1
         #print ('the value of e is ', ee)
         for nn in ee:
          zz = nn & zz
         #print('the value of z before', zz)
         zz = zz - set(scan_square(yy , xx, sudomat))
         #print('the value of scan square is', set (scan_square(yy , xx, sudomat) ))
         #print('the value of z after intersection', len(zz) , '\n\n')
         if len (zz) != 0 :
             identifier = 6
             break

 #print ('the value of identifier is', identifier)
 if identifier == 0 :
     return 1
 else:
     return 0

def solve_predictive (sudomatx):
    sudomatv0 = []
    sudomatv0  = sudomatx
    list_members = []
    for rr in range (9):
        count_zero = 0
        list_members = sudomatx[rr]
        for value in list_members:
            if  value == 0:
              count_zero = count_zero +1
        if count_zero <= 3:
            print ('the row is', rr+1)
            break
    temp_keys = {1,2,3,4,5,6,7,8,9} - set(list_members)
    print('temp keys',temp_keys, '\n')

    for x in temp_keys:
        for jj in range(9):
            if sudomatv0[rr][jj] == 0:
               sudomatv0 = sudoku_update(jj, rr, sudomatv0,x)
               break

    print_sudoku(sudomatx)





#sudomat1_unsolved_test_passed
#matrix = [[0,2,0,0,0,4,3,0,0],[9,0,0,0,2,0,0,0,8],[0,0,0,6,0,9,0,5,0],[0,0,0,0,0,0,0,0,1],[0,7,2,5,0,3,6,8,0],[6,0,0,0,0,0,0,0,0],[0,8,0,2,0,5,0,0,0],[1,0,0,0,9,0,0,0,3],[0,0,9,8,0,0,0,6,0]]

#sudo2matrix-solved
#matrix = [[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,7,9,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]

#sudo2matrix-invert-solved
#matrix = [ [5,6,0,8,4,7,0,0,0],  [3,0,9,0,0,0,6,0,0], [0,0,8,0,0,0,0,0,0], [0,1,0,0,8,0,0,4,0], [7,9,0,6,0,2,0,1,8],[0,5,0,0,3,0,0,9,0], [0,0,0,0,0,0,2,0,0,],  [0,0,6,0,0,0,8,0,7], [0,0,0,3,1,6,0,5,9]]

#sudo3matrix-solved
#matrix = [[1, 2, 0, 6, 0, 8, 0, 0, 0], [5, 8, 4, 2,3, 9, 7, 0, 1], [0, 6, 0, 1, 4, 0, 0, 0, 0], [3, 7, 0, 0, 6, 1, 5, 8, 0], [6, 9, 1, 0, 8, 0, 2, 7, 4], [4, 5, 8, 7, 0, 2, 0, 1, 3], [0, 3, 0, 0, 2, 4, 1, 5, 0], [2, 0, 9, 8, 5, 0, 4, 3, 6], [0, 0, 0, 3, 0, 6, 0, 9, 2]]

#sudo5matrix-solved_test_passed

matrix  = [[3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 8, 0, 0, 9], [0, 7, 0, 2, 6, 0, 0, 0, 5], [0, 5, 0, 0, 0, 0, 0, 3, 1], [8, 0, 3, 0, 9, 0, 7, 0, 6], [2, 6, 0, 0, 0, 0, 0, 9, 0], [5, 0, 0, 0, 2, 6, 0, 8, 0], [6, 0, 0, 1, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 3]]


#sudoku6matrix_unsolved_passed test
#matrix = [[0,3,0,0,2,0,0,8,0] , [4,0,0,8,0,0,0,2,1] , [0,0,0,0,1,0,0,0,0] , [0,0,4,0,0,5,1,3,0] , [7,0,0,0,6,0,0,0,8] , [0,1,8,9,0,0,2,5,6] , [0,0,0,0,5,0,0,0,0] , [6,7,0,0,0,1,0,0,2] , [0,2,0,0,9,0,0,6,0]]


print_sudoku(matrix)
print('\n', 20 * '=')
sudo_num_unsolved(matrix)
print('\n', 20 * '=')


for x in range (9):
   for i in range (9):
       for j in range (9):
           matrix = sudoku_solve_all(i, j, matrix)
           matrix = sudosolve_intellect_lookup( i,j,matrix)
           matrix = sudosolv_vertical(i,j,matrix)
           matrix = sudosolv_horizontal(i,j,matrix)


print_sudoku(matrix)
print('\n', 20 * '=')
sudo_num_unsolved(matrix)
print('\n', 20 * '=')

cccc = validate_sudoku(matrix)
if cccc == 1 :
  print ('the given sudoku is valid')
else:
  print ('the given sudoku is fucked up')

solve_predictive (matrix)
