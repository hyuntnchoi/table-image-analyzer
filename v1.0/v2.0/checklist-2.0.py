import cv2

def init(imagePath):
    print('=== [START] IMAGE READING ===')
    global img
    global rows, cols, channels
    global entireHeight, entireWidth, entireRatio
    global checklistHeight, checklistWidth
    global startX, startY
    global endX, endY
    global rowList, rowHeight, rowColumnList, columnWidthList
    global headObj, bodyObj

    print('img:', imagePath)
    img = cv2.imread(imagePath)

    rows,cols,channels = img.shape

    entireHeight = img.shape[0]
    entireWidth = img.shape[1]
    checklistHeight = 0
    checklistWidth = 0
    startX = 0
    startY = 0
    endX = 0
    endY = 0
    rowList = []
    rowHeight = []
    rowColumnList = []
    columnWidthList = []

    print('>> Entire Height: ', entireHeight) 
    print('>> Entire Width: ', entireWidth)

    print('=== [END] IMAGE READING ===')

def getStartPx():
    print('=== [START] GETTING START PIXEL ===')
    
    global rows
    global cols

    for i in range(rows):
        for j in range(cols):
            px = img[i,j]
            if all(px < [200,200,200]):
                nextPx = img[i+1,j]
                if all(nextPx < [200,200,200]):
                    global startX
                    global startY
                    startY = i
                    startX = j
                    print('>> Start X : ', startX)
                    print('>> Start Y : ', startY)
                    return
 
    print('=== [END] GETTING START PIXEL ===')

def getRows():
    print('=== [START] GETTING ROWS ===')
    rowCnt = 0
    global startY
    global rowList
    y = startY
    rowList = []
    
    while y <= rows:
        nPx = img[y, startX+1]
        nnPx = img[y, startX+2]
        nnnPx = img[y, startX+3]
        nnnnPx = img[y, startX+4]
        if all(nPx < [200,200,200]) and all(nnPx < [200,200,200]) and all(nnnPx < [200,200,200]) and all(nnnnPx < [200,200,200]):
            print('>> Row detected')
            rowList.append([startX, y])
            #print(rowList)
            y = y + 3
        else:
            y += 1
        if y == rows-1:
            print('>> Created row count: ', len(rowList))
            break
    print('=== [END] GETTING ROWS ===')

def setEndY():
    print('=== [START] END Y SETTING ===')
    
    global endY
    
    if len(rowList) > 0:
        endY = rowList[-1][1]
        print('>> End Y :', endY)
    else:
        print('>> RowList is empty')
        print('>> End Y setting failed')
    
    print('=== [END] End Y setting ===')

def getChecklistHeight():
    print('=== [START] CHECKLIST ENTIRE HEIGHT SETTING ===')
    
    global checklistHeight
    global endY

    checklistHeight = endY-startY
    
    print('>> Checklist Height :', checklistHeight)
    print('=== [END] CHECKLIST ENTIRE HEIGHT SETTING ===')

def getChecklistWidth(): 
    print('=== [START] CHECKLIST ENTIRE WIDTH SETTING ===')
    
    global endX
    global startX
    global checklistWidth
    x = startX
    y = startY

    while x <= cols:
        x += 1
        curPx = img[y, x]
        nextPx = img[y, x+1]
        
        #if next pixel is white,
        #check below pixels of current pixel
        #and if the pixels are black
        #current pixel is last pixel of entire row
        if all(nextPx > [200,200,200]):
            bPx = img[y+1, x]
            bbPx = img[y+2, x]
            bbbPx = img[y+3, x]
            bbbbPx = img[y+4, x]
            if all(bPx < [200,200,200]) and all(bbPx < [200,200,200]) and all(bbbPx < [200,200,200]) and all(bbbbPx < [200,200,200]):
                endX = x
                checklistWidth = endX - startX
                print('>> End X: ', endX)
                print('>> Checklist Width :', checklistWidth)
                break
    
    if endX == 0: 
        print('>> Failed to set checklist width')
    print('=== [END] CHECKLIST ENTIRE WIDTH SETTING ===')


def getRatioBetweenRows():
    print('=== [START] CHECKLIST HEIGHT RATIO BTW ROWS ===')
    
    i = 0
    global rowHeight
    rowHeight = []

    for row in rowList:
        if len(rowList)-1 == i:
            height = 0
            rowHeight.append(height)
            break
        else:
            y1 = rowList[i][1]
            y2 = rowList[i+1][1]
            height = y2 - y1
            rowHeight.append(height)
        
        i += 1
    
    print('>> Row Height:', rowHeight)
    print('=== [END] CHECKLIST HEIGHT RATIO BTW ROWS ===')

def getRowColumns(row):
    print('=== [START] GETTING ROW COLUMNS ===')    
    
    global endX
    global rowColumnList
    tempList = []
    x = row[0]+2 #as 2 pixels usually used in starting point
    y = row[1]

    tempList.append(x) #insert start x in list 

    while x < endX:
        x += 1
        
        curPx = img[y, x]
        bPx = img[y+1, x]
        bbPx = img[y+2, x]
        bbbPx = img[y+3, x]
        
        if all(bPx < [200,200,200]):
            if all(bbPx < [200,200,200]):
                if all(bbbPx < [200,200,200]):
                    tempList.append(x)
                    x += 2
    
    rowColumnList.append(tempList)
    print('>> rowColumnList :', rowColumnList)

    print('=== [END] GETTING ROW COLUMNS ===')    

def getColumnWidth(row):  
    print('=== [START] GETTING COLUMN WIDTH ===')
    print(row)  
    global columnWidthList
    tempList = []
    i = 0
    
    while i < len(row) - 1:
        width = row[i+1] - row[i]
        tempList.append(width)
        i += 1

    columnWidthList.append(tempList)
    print('>> columnWidthList :', columnWidthList)

    print('=== [END] GETTING COLUMN WIDTH ===')

def sumRowHeight(rowList, startIdx, endIdx):
    sum = 0
    for i in range(int(startIdx), int(endIdx), 1):
        #print("start idx : " + str(startIdx) + " | end idx : " + str(endIdx))
        try:
            sum += rowList[i]
        except IndexError:
            error = input('out of index 에러 발생. 이미지의 row 개수를 다시 확인해 주세요')
            
    return sum

def getEntireRatio(bodiesCnt):
    global checklistHeight
    global headObj, bodyObj
    arr = []
    
    lastPos = int(headObj['rowCnt'])
    #print('lastPos type:' + str(type(lastPos)))
    
    headObj['totalHeight'] = sumRowHeight(rowHeight, 0, lastPos)

    arr.append(str(headObj['totalHeight']) + '/' + str(checklistHeight)) 
    
    for x in range(int(bodiesCnt)):
        rowCnt = int(bodyObj['body' + str(x)]['rowCnt'])
        #print('rowCnt type:' + str(type(rowCnt)))
        
        #print('last pos:' + str(lastPos) + ' | row count:' + str(rowCnt))
        
        bodyObj['body' + str(x)]['totalHeight'] = sumRowHeight(rowHeight, lastPos, lastPos+rowCnt)

        ttlHeight = bodyObj['body' + str(x)]['totalHeight']

        arr.append(str(ttlHeight) + '/' + str(checklistHeight))

        lastPos = lastPos + rowCnt
        
    return str(arr).replace("'", "")

def display(headEndRow,headRowCnt,headColCnt,bodyObj,bodiesCnt,x,y):
    global entireRatio
    global headObj
    
    print("======COPY/PASTE======\n")
    
    for i in range(int(bodiesCnt)):
        obj = bodyObj['body'+str(i)]
        rowCnt = str(obj['rowCnt']).replace("'", "")
        colCnt = str(obj['colCnt']).replace("'", "")
        rowRatio = str(obj['rowRatio']).replace("'", "")
        colRatio = str(obj['colRatio']).replace("'", "")
        
        print("bodyObj.body" + str(i) + " = {")
        print("    rowCnt: " + rowCnt + ",")
        print("    colCnt: " + colCnt + ",")
        print("    rowRatio: " + rowRatio + ",")
        print("    colRatio: " + colRatio + ",")
        print("};")
        print("\n")

    headRowRatio = str(headObj['rowRatio']).replace("'", "")
    headColRatio = str(headObj['colRatio']).replace("'", "")

    entireRatio = getEntireRatio(bodiesCnt)
    
    print("const cl = new CheckListWithImageBuilder()")
    print("                .setDivId('myCanvas')")
    print("                .setEntireRatio(" + entireRatio + ")")
    print("                .setHeadRowCnt(" + headRowCnt + ")")
    print("                .setHeadColCnt(" + headColCnt + ")")
    print("                .setHeadRowRatio(" + headRowRatio + ")")
    print("                .setHeadColRatio(" + headColRatio + ")")
    print("                .howManyBodies(" + bodiesCnt + ")")
    print("                .setChildBodiesRowCol(bodyObj)")
    print("                .setStartX(" + str(x) + ")")
    print("                .setStartY(" + str(y) + ")")
    print("                .setTest(true)")
    print("                .build();\n")

    print("======COPY/PASTE======")

def main():
    global headObj, bodyObj
    global entireRatio
    
    print('>>분석할 이미지 경로를 입력해 주세요:')
    img = input()
    init(img);
    getStartPx();
    getRows();
    setEndY();
    getChecklistHeight();
    getChecklistWidth();
    getRatioBetweenRows();

    for row in rowList:
        getRowColumns(row);

    for row in rowColumnList:
        getColumnWidth(row);

    print('======================================')
    print('===분석이 성공적으로 완료되었습니다===')
    print('======================================')
    
    print('>>이미지 전체 넓이:', entireWidth)
    print('>>이미지 전체 높이:', entireHeight)
    print('>>점검표 전체 넓이:', checklistWidth)
    print('>>점검표 전체 높이:', checklistHeight)
    print('>>시작 지점: [',startX,',',startY,']')
    print('>>ROW 총 개수:', len(rowList))
    print('>>ROW 간의 높이:')
    i = 0
    for row in rowHeight:
        if i < len(rowHeight) - 1:
            print('row',i+1,' - row',i,': ',row,'px')
            i += 1
    
    print('>>각 ROW 마다의 COLUMNS 넓이:')
    j = 0
    for row in columnWidthList:
        if j < len(columnWidthList) - 1:
            print('row',j,' columns width:',row)
            j += 1

    # set head
    headObj = {}

    headEndRow = input('1. head는 몇 번째 row까지 입니까?')
    headRowCnt = input('1-1. head는 몇 개의 row로 이루어져 있습니까?')
    headColCnt = input('1-2. head는 몇 개의 컬럼으로 이루어져 있습니까?')

    headObj['rowCnt'] = headRowCnt
    headObj['colCnt'] = headColCnt
    headObj['rowRatio'] = []
    headObj['colRatio'] = []
    
    headHeight = sumRowHeight(rowHeight, 0, headEndRow)
    for x in range(int(headRowCnt)):
        headObj['rowRatio'].append(str(rowHeight[x]) + '/' + str(headHeight))

    headColArr = columnWidthList[0]
    for col in headColArr:
        headObj['colRatio'].append(str(col) + '/' + str(checklistWidth))
    
    # set bodies
    bodyObj = {}
    rangeStart = int(headEndRow)

    bodiesCnt = input('2. body는 몇 개로 이루어져 있습니까?')
    
    for k in range(int(bodiesCnt)):
        bodyObj['body'+str(k)] = {}
        bodyObj['body'+str(k)]['rowCnt'] = input(str(k+1)+'번째 body의 row는 몇 개로 이루어져 있습니까?')
        print(bodyObj)
        bodyObj['body'+str(k)]['colCnt'] = input(str(k+1)+'번째 body의 column은 몇 개로 이루어져 있습니까?')
        print(bodyObj)
        bodyObj['body'+str(k)]['rowRatio'] = []
        bodyObj['body'+str(k)]['colRatio'] = []
                    
        rowCnt = bodyObj['body'+str(k)]['rowCnt']
        rangeEnd = rangeStart + int(rowCnt)
        height = sumRowHeight(rowHeight, rangeStart, rangeEnd)
        
        idx = rangeStart
        for x in range(int(rowCnt)):
            bodyObj['body'+str(k)]['rowRatio'].append(str(rowHeight[idx]) + '/' + str(height))
            idx += 1

        rangeStart = rangeEnd #for next loop
        
        rowForColWidth = input('몇 번째 row의 column 넓이 배열을 기준으로 현재 body의 column을 나누겠습니까?')
        arrForColWidth = columnWidthList[int(rowForColWidth)]
        for col in arrForColWidth:
            bodyObj['body'+str(k)]['colRatio'].append(str(col) + '/' + str(checklistWidth))
                          
    display(headEndRow,headRowCnt,headColCnt,bodyObj,bodiesCnt,startX,startY)
         
main();
    
close = input('press close to exit')
