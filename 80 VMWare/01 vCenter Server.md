### 安裝說明：
<img width="550" height="422" alt="image" src="https://github.com/user-attachments/assets/fd836219-dd67-4064-a8c7-5f36988850a9" />

1. vCenter Server依上圖概略可區分成以下幾個區塊：硬體、作業系統、Platform Services Controller ( PSC ) Group of Services、
vCenter Server Group of Services及DB。

2. PSC Group of Services包含Single Sign-On、License service、Lookup Service及VMware Certificate Authority等服務；
vCenter Server Group of Services包含vCenter Server、vSphere Web Client、Inventory Service...等服務。

3. 在6.x的版本之前，vCenter可選擇安裝於實體機或虛擬機、windows或linux，且PSC、vCenter Server Group及DB可另安裝於不同主機上，
但於7.x版本開始，VMware將所有元件全部打包起來，只能安裝於虛擬機Linux系統上。

4. vCenter安裝之Linux系統，是經VMware調整過之系統，其稱之為Photon OS。

5. vCenter採用VMware的部署範本方式安裝，但其部署方式與部署VM略有不同。部署vCenter時，區分二個階段。第一階段是先建置VM；
第二階段則是將此VM開啟，並針對vCenter做其系統設定。
<img width="897" height="414" alt="image" src="https://github.com/user-attachments/assets/341eb41d-d31c-46d7-b90c-71be2e0692ab" /><img width="902" height="436" alt="image" src="https://github.com/user-attachments/assets/53133d72-6f47-45f1-b751-770d84053552" />

### 安裝步驟：
1. 執行vCenter Server Installer，點擊Install，接著依預設值至下一點。
<img width="1109" height="700" alt="image" src="https://github.com/user-attachments/assets/0f8cf5a2-293b-42b9-92ff-ead9e698d055" />

2. 此步驟需輸入ESXi的IP及其帳號密碼，依ESXi建置時設定：
> - ESXi host or vCenter Server name：10.5.10.218
> - User name：root
> - <img width="1109" height="700" alt="image" src="https://github.com/user-attachments/assets/a4dde4f8-89e9-4bc0-ae2c-1b985888fced" />

3. 接著律定vCenter Server Root密碼。
   
4. 決定vCenter部署大小，可依實際需求做調整。
<img width="1109" height="700" alt="image" src="https://github.com/user-attachments/assets/a8cc3b61-7e29-4665-9771-2f5ebed5c40b" />

5. 選擇vCenter存放之磁碟位置，因先前建置ESXi時並無新增其他儲存區，故畫面上僅有本機儲存區。
<img width="1109" height="700" alt="image" src="https://github.com/user-attachments/assets/f8642bd2-910d-449a-8d30-c5b587d9b0d8" />

6. Network選到mgmt，輸入之IP需屬於mgmt之網段，輸入完下一步核對設定無誤後即開始vCenter第一階段安裝部署。
> - IP address：10.5.10.239
> - Subnet mask or prefix length：24
> - Default gateway：10.5.10.254
> - DNS servers：8.8.8.8
> - ( 以上設定依實際情形調整 )
<img width="1125" height="883" alt="image" src="https://github.com/user-attachments/assets/ee7f5bbd-7413-4f37-9f61-17bda1f8c12b" />

7. 第二階段安裝，先設定時間同步(NTP)，依預設值與ESXi同步即可

8. 接著設定SSO( Single Sign-On ) configuration，這邊的Domain是vCenter的Domain而非AD Domain，若組織有多部vCenter Server，就可改用Join an existing SSO domain的方式，如此便可以單一帳號管理多部vCenter Server，此模式稱作Enhanced Linked Mode，下面先以單一vCenter方式設定，設定完後續依預設按下一步即開始安裝。
> -  Single Sign-On domain name：vsphere.local
> -  <img width="1125" height="883" alt="image" src="https://github.com/user-attachments/assets/0eeb527a-6d31-4149-af4d-3764511dd952" />

9. 安裝完成後，瀏覽器輸入IP或FQDN即可進入vSphere Client的網頁管理介面；若加上port：5480，則進入vCenter Server管理介面。一般在管理ESXi及虛擬機時，都是登入vSphere Client管理。

### vSphere Client：
<img width="1920" height="1055" alt="image" src="https://github.com/user-attachments/assets/89b0bf75-2853-474f-8402-700adeb98901" />

1. 登入vSphere Client後，左方為其導覽窗格，導覽窗格為物件分類頁籤，由左至右依序：
> - 主機和叢集
> - 虛擬機器和範本
> - 儲存區
> - 網路

2. 導覽窗格顯示之圖示為其分類所屬物件，右邊則顯示選取物件之資訊屬性。目前畫面位於「主機和叢集」頁籤，並只有「10.5.10.239」此vCenter物件。

3. 於vCenter物件右鍵「新增資料中心」，資料中心以其預設Datacenter命名。

4. Datacenter物件右鍵「新增主機」，將ESXi新增進去，IP：10.5.10.218，輸入ESXi的帳號密碼，餘依預設值繼續即完成主機新增。

5. 此時除可看到新增之主機物件，還會有一個vCenter虛擬機物件。
再於Datacenter物件右鍵「新增叢集」，名稱：cluster，餘功能均先關閉。產生叢集物件後，將先前產生之主機物件拖曳至cluster底下。

6. 叢集主要有三個功能，分別為DRS、HA及vSAN，此功能將套用於其下之主機。之所以將新增之主機拖曳至叢集，而非直接於叢集底下
新增主機，主因為於叢集底下新增主機，該主機會強制進入維護模式，造成主機內之虛擬機關機，若於Datacenter完成新增主機後，
再拖曳進去則無此問題。

7. vCenter安裝步驟7設定vCenter的時間同步與ESXi同步，但先前安裝ESXi時並未設定NTP Server，因此接續便於vSphere Client設定ESXi主機的NTP Server。
點擊加入之ESXi主機物件，右邊畫面切至「設定」頁籤，下方展開「系統」區塊，點擊「時間組態」，右上方點擊「編輯」，輸入以下資訊：
使用網路時間通訊協定(啟用NTP用戶端)
> - NTP伺服器：time.asia.apple.com
> - 啟動NTP服務：checked
> - 如此即完成vCenter安裝並加入ESXi主機集中管理。

8. 如此即完成vCenter安裝並加入ESXi主機集中管理。

### vCenter帳號認證及權限：
1. 使用者登入vSphere Client示意圖如下：
> - <img width="463" height="552" alt="image" src="https://github.com/user-attachments/assets/0a186a8b-1124-4c5a-9daa-0cf254a8bd0b" />
> - 使用者連至vSphere Client並輸入帳密登入後，其會將資料交由SSO服務驗證，驗證無誤後便會核發SAML token，讓使用者可進入此vCenter Server去管理其下主機

2. AD認證： vCenter雖已有其自身Domain及帳號管理服務，但仍可結合AD，以AD做為帳號驗證之依據，步驟如下：
> a. vSphere Client -> 功能表 -> 系統管理，於左方導覽窗格選擇「組態」，右方畫面選擇「Active Directory 網域」，再點擊「加入AD」。
> 
> b. 於彈出的畫面輸入AD網域及驗證AD的使用者名稱、密碼，加入AD後vCenter會需要重開機，重開機請至vCenter Management頁面(IP:5480)做系統重開機，而非於vSphere Client操控vCenter的虛擬機重開機。
> c. 完成vCenter重開機後連至vSphere Client時，請仍以原vCenter帳號登入，而非AD帳號。
> 
> d. 登入後一樣進到系統管理的「組態」畫面，此時右邊畫面選到「身份識別來源」，右邊點選「新增」，彈出視窗確認身份識別來源類型是否為「Active Directory」；網域名稱是否為先前新增之域名，無誤後新增，AD域名即會列在畫面表格內。
> 
> e. 左方導覽窗格選到「使用者和群組」，右邊網域下拉選單選到新增的域名，可確認下方表格是否有將AD帳號列出。
> 
> f. 左方導覽窗格選到「全域權限」，右邊點擊「+」會彈出新增權限視窗，網域選到新增的AD網域，輸入使用者名稱，選擇所需的角色，勾選「散佈到子系」，即可以此AD帳號登入vSphere Client。


3. 權限區分：
> a. vSphere Client的帳號權限區分「物件權限」及「全域權限」二類，在2.6點針對AD帳號新增的權限是屬全域權限。
> 
> b. 新增物件權限方式可於vSphere Client畫面從「主機和叢集」、「虛擬機器和範本」、「儲存區」及「網路」底下，選取任一物件，畫面右邊再切換至「權限」頁籤，此介面與全域權限之介面相同，但於此新增之權限屬物件權限。
> 
> c. 各權限判斷的原則為「小範圍權限蓋過大範為權限」，也就是說物件權限優先全域權限；底層物件權限高於上層物件權限。
> 
> e.g.：全域權限設定帳號test具唯讀權限，於ESXi主機物件，設定帳號test具系統管理員權限，則test登入將具管理ESXi主機權限。
        vCenter物件權限設定帳號test具唯讀權限；底層cluster權限具系統管理員權限，則test登入可管理cluster物件。

### Enhanced Linked Mode：
1. 先前在安裝vCenter Server時便已提到Enhanced Linked Mode，此模式是考量到一個組織可能有多部vCenter Server，為了便於管理而設計的。
2. 當安裝第二台或多台vCenter Server時，於安裝步驟8可將新安裝的vCenter Server加入到已存在的vCenter Server，如此不論連哪一部vSphere Client，
只要具有權限，vSphere Client畫面便會有各台vCenter Server及其下之ESXi和VM。
3. 要使用Enhanced Linked Mode，vCenter建議使用相同版本，至少版本不能落差太高，且不同版本間的相容性，於安裝設定時可能都會遭遇不同的狀況。
4. 若單位已有多部vCenter Server且未使用Enhanced Linked Mode，是無法另行調整設定加入此模式，只能將vCenter Server重新建置再啟用。
5. 在單一vCenter Server時，全域權限與vCenter的物件權限所影響的層級是一樣的。但當有多部vCenter Server且啟用Enhanced Linked Mode時，
全域權限可決定帳號具有哪些vCenter的管理權限，而vCenter物件權限僅只能影響該vCenter所屬底下之物件。
<img width="911" height="690" alt="image" src="https://github.com/user-attachments/assets/4a733116-e660-4c7d-b7db-d8e038369230" />
