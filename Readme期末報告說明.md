---
title: 軟體工程期末報告說明
---

# 報告說明

DEMO影片網址:https://youtu.be/n2gb6Lq_vJQ

## 最後大致分工
```
+黃太陽:很多API、前端設計建議、後端學習、前端後端指導、資料庫設計&建議、DEMO影片錄製。
+鄭翊宏:測試人員、框架製作、heroku發佈、session處理、登入逾時處理、
        (寄信、寄驗證碼、設驗證碼、重設密碼、確認密碼、增加教室、刪除教室、
		登入、改設備、申請管理員)、看全部user、(查看、確認、拒絕)管理員申請、
		查看申請狀況、選擇教室、查看info、查看全部管理員)等API製作。
+謝翔宇:API撰寫、後端學習、資料庫設計&建議。
+吳承遠:登入模組、降級模組、註冊模組、忘密碼模組、查/改借用人頁面及借用申請頁面(改查人資模組)、申請模組。
+孟羽真:測試幹部、學習前端技術、檢視歷史頁面、管理員升級功能頁面、修改個人資料頁面、
	確認借用人申請頁面、確認歸還教室頁面、確認借出教室頁面、CSS-RWD。
+林欣儀:檢視教室狀態頁面、借教室頁面、新增刪除教室頁面、修改教室狀態頁面、前端學習。
```
https://trello.com/b/HLH2FZ4K/ntou%E6%95%99%E5%AE%A4%E5%80%9F%E7%94%A8%E5%B9%B3%E5%8F%B0

## 提升流程品質或系統品質措施(如Trevis-CI、JMeter、JWT等)
```
+新增註解，幫助使用者在借教室的時候和管理者在修改教室狀態時有紅、黃、綠三種顏色分辨教室狀態。
+使用redis處理session問題
+有使用CD工具(持續部屬工具)Heroku，在遠端布置資料庫
+使用Postman做為測試API的工具
```

## 未達成的清單
```
-race condition 處理
```
