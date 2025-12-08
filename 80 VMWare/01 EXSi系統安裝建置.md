##### 1. 透過 IMM 或 iLO 連線伺服器，掛載ESXi ISO檔案，照預設步驟即可完成安裝並進入ESXi DCUI ( Direct Console User Interface )畫面設定。
安裝期間會要求設定root密碼。
<img width="1024" height="766" alt="image" src="https://github.com/user-attachments/assets/eb789f86-ccea-4582-b47e-4868f856374b" />

##### 2. 安裝完時，ESXi會以DHCP方式獲取無效IP，故按「F2」進入系統設定，選「Configure Management Network」修改ESXi網路設定。
> a. Network Adapters：vmnic0、vmnic1
> 
> b. VLAN (optional)：931
> 
> c. IPv4 Configuration：
>> - set static IPv4 address and network configuration：
>>>> - IPv4 Address：10.5.10.218
>>>> - Subnet Mask：255.255.255.0
>>>> - Default Gateway：10.5.10.254
>>>> - ( 以上IP設定依實際狀況進行調整 )
>
> d. DNS Configuration：
>> - Use the following DNS server addresses and hostname：
>>>> - Primary DNS Server：8.8.8.8
>>>> - Alternate DNS Server：168.95.1.1
>
> e. 設定完Esc離開時，系統會要求重啟網路服務，重啟網路服務後，跳板機若與ESXi同網段，即可以瀏覽器連線至ESXi伺服器做後續設定。
> 
> f. 若跳板機與ESXi分屬不同Vlan，則需以ESXi Shell方式，輸入指令設定。
>> 1. Troubleshooting Options -> Enable ESXi Shell
>> 2. 「Alt + F1」會將畫面切換至命令模式，輸入帳號密碼登入。
>> 3. esxcli network vswitch standard policy failover set -v vSwitch0 -l iphash -a vmnic0,vmnic1            // 代表將vmnic0、1兩張網卡設定成failover，並使用iphash方式路由
>> 4. esxcli network vswitch standard portgroup policy failover set -p "Management Network" -u           // -u 代表將Management Network連接埠群組繼承vSwitch設定
>> 5.  上述指令輸入完，其他網段設備即可存取ESXi，按「Alt + F2」回到原DCUI畫面即可，後續第3點可不用執行。

##### 3. 以瀏覽器登入ESXi後，左方面版導覽器選「網路」，右方畫面切換頁籤至「虛擬交換器」，點擊進入「vSwitch0」設定畫面，再點擊新增上行，確認vmnic0及vmnic1加入後，將「NIC整併」展開，負載平衡欄位切換至「根據IP雜湊進行路由」後儲存。

##### 4. 於vSwitch拓樸處修改「Management Network」設定，將「NIC整併」展開，負載平衡欄位切換至「從vSwitch繼承」後儲存，儲存後其他網段即可連線至ESXi伺服器。
<img width="1664" height="559" alt="image" src="https://github.com/user-attachments/assets/996f2b27-1935-42f3-a477-af84aa9b2094" />

##### 5. 左方面版導覽器選「網路」，右方畫面切換頁籤至「連接埠群組」，點擊新增「新增連接埠群組」，彈出視窗輸入以下內容：
> - 名稱：mgmt
> - VLAN：931
> - 虛擬交換器：vSwitch0
> - 安全性：從vSwitch繼承

##### 6. 後續建立vCenter Server時，將使用此連接埠群組。至於其餘網路、儲存區設定，將俟vCenter Server安裝完後再行設定。

## 網路設定說明：
<img width="900" height="578" alt="image" src="https://github.com/user-attachments/assets/fdd4954b-c8e9-4171-874a-69f8506da5ab" />

1. 實體主機ESXi網卡，VMware的命名為vmnic，其會連接交換器以獲取網路服務。

2. ESXi內可建立許多虛擬機(VM)，而VMware為了讓虛擬機能連接不同的網段，故設計了vSphere Standard Switch ( VSS )的虛擬交換器服務，
VSS對VM的連接埠定義為port group；對實體伺服器的管理或儲存區連接等系統管理功能連線則使用kernel port。不論哪一種類型連接埠，
均可指派不同的Vlan，令VM或實體機連接不同網段上。

3. Kernel Port是不能用來建立VM使用，就算其他VM與kernel port是同一網段，仍需另建一組port group，
故系統安裝設定第5點才說明將vCenter Server 安裝於mgmt上。

4. VM除了使用port group方式獲取網路，亦可直接使用實體機上網卡( Direct Path I/O )，單獨使用一固定網路線路，此模式雖可有獨立之頻寬，
但會有許多VM之功能不能使用，例：快照、vMotion、暫停/繼續...。此模式不同於原VM上之網路設定，需於ESXi啟用PCI網卡裝置，始能
於VM新增PCI狀置，啟用獨立網路。

5. 在網路管理時，有時會做封包側錄，此時會在交換器上設定Port Mirror以抄寫所需封包，但在VSS上並不支援此功能。此功能在vCenter
Distribution Switch上才有支援；而VSS若要封包複寫，可於安全性原則啟用混合模式( Promiscuous Mode )，此模式類似將Switch降級成HUB，
故在同一Vlan上，其封包是採用廣播的模式傳送，而非mac對mac點對點方式傳送。

6. VSS連接實體機的網卡稱為「上行介面卡 ( Uplink )」，為了提升網路傳輸速率及可靠性，VSS可連接多個實體網卡( NIC Teaming )，並設定負載平衡。
負載平衡設定方式可參考「系統安裝設定 - 3、4」，區分以下類型：

> a. IP雜湊 ( IP Hash )：依據來源IP及目的IP來決定封包傳輸路徑。
> 
> b. MAC雜湊 ( MAC Hash )：依據來源Mac決定封包傳輸路徑。
> 
> c. 連接埠ID：依據來源連接埠ID決定封包傳輸路徑。

7. Mac Hash與連接埠ID的負載平衡模式，在一般情況下是相同的功能，因每個port id只會對映到一台VM，對映到一個mac address，但若是有
槽狀虛擬化，則2者就會有不同的判斷路徑。

8. VSS上會設定一些如：負載平衡模式、安全性、流量控管...等等功能或限制，此為預設原則( Default Policy )，參考設定步驟如：系統安裝設定
2.f.iii及第3點；預設原則設定完須再於port group定義有效原則( Effective Policy )，此原則可繼承預設原則或另行設定新的原則，兩者原則若有牴觸，
以生效原則為主，參考設定步驟如：系統安裝設定2.f.iv及第4點。
<img width="785" height="560" alt="image" src="https://github.com/user-attachments/assets/1f914671-f787-43c6-a6d8-2bdcbcf4620e" />




