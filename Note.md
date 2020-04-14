# アプリのフロー（想定）



1. 前処理
2. OCR
3. S3に保存

## 1. 前処理
目的
OCRの精度向上

アプローチ
- 写真から植物のプレートのみを取得し、プレートの形を補正
  - 四角を抽出
    - 直線検出
      - エッジ検出
      - パラメータ空間に変換
  - 色で抽出
    - 天気や撮影時間に左右されないか？
- 文字領域を抽出し、最左上、右上、左下、右下を探し出し、トリミング
  - これだと台形補正ができなそう
- +α
  - 帳票分類

輪郭検出
- OpenCV
- DeepLearning


メモ
- 前処理
  - マスク
    - エッジ検出するにしても、前処理で不要な箇所はマスクしたい
    - 色
      - RGBに一定の閾値を設けて、マスク
        - ⇨プレートだけ、目立つようにはできなかった。
      - Greenにだけ一定の閾値を設けて、マスク
        - ⇨プレートだけ、目立つようにはできなかった。
      - RGBの各値のレンジを設け、マスク
- 二値化
  - 適応的二値化処理
  - 大津の二値化処理
- 輪郭の近似
- エッジ検出
  - 方法
    - 勾配法
    - ラプラシアン法
    - ソーベル法
    - ガウスのラプラシアン法
  - canny
  -  前処理
     -  binary gradient mask
     -  dilated gradient mask
     -  refrence
        -  https://jp.mathworks.com/discovery/edge-detection.html
-  文字領域抽出
   -  MSER
- 直線検出
  - （確率的）ハフ変換
    - 前処理が必要そう
      - ブラー
      - 二値化
  - LSD
- 領域検出
  - 大津の2値化
- 参考資料
  - http://agora.ex.nii.ac.jp/~kitamoto/research/publications/k:tric06y.pdf
  - http://www2.riken.jp/brict/Yoshizawa/Lectures/IP2011/Lec24.pdf

  



## Others

### アプリ機能のidea

- 植物の名前検出



### プレートの色情報

20200412_1

- RGB（0x）
  - 165c51
- BGR
  -  81,92,22