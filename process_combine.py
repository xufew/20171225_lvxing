# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============
import sys

import pandas as pd


if __name__ == '__main__':
    inputList = sys.argv
    outPath = sys.argv[-1]
    finalFrame = []
    for filePath in inputList[1:-1]:
        useFrame = pd.read_table(filePath, sep=',')
        if len(finalFrame) == 0:
            finalFrame = useFrame
        else:
            finalFrame = pd.merge(
                    finalFrame, useFrame, how='outer', on='userid'
                    )
    finalFrame.to_csv(outPath, index=False)
