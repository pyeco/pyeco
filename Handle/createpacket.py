#!/usr/bin/python
# -*- coding: utf-8 -*-
#License BSD
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from Socket.DataAccessControl import DataAccessControl

ACCESORY_TYPE_LIST = ["ACCESORY_NECK",
				"JOINT_SYMBOL",
				]
UPPER_TYPE_LIST = ["ARMOR_UPPER",
				"ONEPIECE",
				"COSTUME",
				"BODYSUIT",
				"WEDDING",
				"OVERALLS",
				"FACEBODYSUIT",
				]
LOWER_TYPE_LIST = ["ARMOR_LOWER",
				"SLACKS",
				]
RIGHT_TYPE_LIST = ["CLAW",
				"HAMMER",
				"STAFF",
				"SWORD",
				"AXE",
				"SPEAR",
				"HANDBAG",
				"GUN",
				"ETC_WEAPON",
				"SHORT_SWORD",
				"RAPIER",
				"BOOK",
				"DUALGUN",
				"RIFLE",
				"THROW",
				"ROPE",
				"BULLET",
				"ARROW",
				]
LEFT_TYPE_LIST = ["BOW",
				"SHIELD",
				"LEFT_HANDBAG",
				"ACCESORY_FINGER",
				"STRINGS",
				]
BOOTS_TYPE_LIST = ["LONGBOOTS",
				"BOOTS",
				"SHOES",
				"HALFBOOTS",
				]
PET_TYPE_LIST = ["BACK_DEMON",
				"PET",
				"RIDE_PET",
				"PET_NEKOMATA",
				]
class CreatePacket(DataAccessControl):
	def init(self, serverobj):
		serverobj.setlibdic(serverobj.libdic, self)
		self.add("pack", self.netio.pack)
		self.add("packstr", self.netio.packstr)
	
	def create0002(self, clientver):
		"""認証接続確認(s0001)の応答"""
		datatype = "0002"
		datacontent = "0000"+clientver
		return datatype, datacontent
	
	def create001e(self):
		"""PASS鍵"""
		datatype = "001e"
		datacontent = "3030303030303030"
		return datatype, datacontent

	def create000b(self, recvcontent):
		"""接続・接続確認(s000a)の応答"""
		datatype = "000b"
		datacontent = recvcontent
		return datatype, datacontent
	
	def create0020(self, command):
		"""アカウント認証結果/ログアウト開始/ログアウトキャンセル"""
		datatype = "0020"
		datacontent = ""
		if command == "loginsucess":
			datacontent = "00000000"+"00000000"+"00000000"+"00000000"
			#認証成功
		elif command == "loginfaild":
			datacontent = "FFFFFFFE"+"00000000"+"00000000"+"00000000"
			#認証失敗
		elif command == "isonline":
			datacontent = "FFFFFFFB"+"00000000"+"00000000"+"00000000"
			#既にログインしています
		elif command == "logoutstart":
			datacontent = "00"
			#ログアウト開始
		elif command == "logoutcancel":
			datacontent = "f9"
			#ログアウトキャンセル
		return datatype, datacontent
	
	def create0028(self, pc):
		"""4キャラクターの基本属性"""
		datatype = "0028"
		datacontent = ""
		datacontent += "04"#キャラ数
		name = pc.name.encode("hex")
		namelength = str(int(len(name)/2))
		datacontent += self.pack(namelength, 2)#名前の長さ#全角ならx3
		datacontent += name+"000000"#名前
		datacontent += "04"+self.pack(pc.race, 2)+"000000"#種族#最初の01はあとのデータの長さ（以下略）
		datacontent += "04"+self.pack(pc.form, 2)+"000000"#フォーム（DEMの）
		datacontent += "04"+self.pack(pc.gender, 2)+"000000"#性別
		datacontent += "04"+self.pack(pc.hair, 4)+"0000"#髪型
		datacontent += "00000000"#不明
		datacontent += "04"+self.pack(pc.haircolor, 2)+"000000"#髪色
		datacontent += "04"+self.pack(pc.wig, 4)+"0000"#ウィング#ない時はFFFF
		datacontent += "00000000"#不明
		datacontent += "04"+"FF"+"000000"#不明
		datacontent += "04"+self.pack(pc.face, 4)+"000000000000"#顔
		datacontent += "04"+self.pack(pc.base_lv, 2)+"000000"#転生前のレベル#付ければ上位種族になる
		datacontent += "04"+self.pack(pc.ex, 2)+"000000"#転生特典？
		#if pc.race = 1 than pc.ex = 32 or 111+
		datacontent += "04"+self.pack(pc.wing, 2)+"000000"#転生翼？
		#if pc.race = 1 than pc.wing = 35 ~ 39
		datacontent += "04"+self.pack(pc.wingcolor, 2)+"000000"#転生翼色？
		#if pc.race = 1 than pc.wingcolor = 45 ~ 55
		datacontent += "04"+self.pack(pc.job, 2)+"000000"#職業
		datacontent += "04"+self.pack(pc.map, 8)#マップ
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "04"+self.pack(pc.lv_base, 2)+"000000"#レベル
		datacontent += "04"+self.pack(pc.lv_job1, 2)+"000000"#1次職レベル
		datacontent += "04"+"0003"+"0000"#残りクエスト数
		datacontent += "00000000"#不明
		datacontent += "04"+self.pack(pc.lv_job2x, 2)+"000000"#2次職レベル
		datacontent += "04"+self.pack(pc.lv_job2t, 2)+"000000"#2.5次職レベル
		datacontent += "04"+self.pack(pc.lv_job3, 2)+"000000"#3次職レベル
		#while len(datacontent) < 300:
		#	datacontent += "00"
		return datatype, datacontent
	
	def create0029(self, pc):
		"""4キャラクターの装備"""
		datatype = "0029"
		datacontent = ""
		datacontent += "0d"#変わらないらしい----キャラ0
		cachetype,cache = self.create09e9(pc)
		cache = cache[10:-36]
		datacontent += cache
		datacontent += "0d"#変わらないらしい----キャラ1
		datacontent += "00000000"#頭
		datacontent += "00000000"#頭アクセサリ
		datacontent += "00000000"#顔
		datacontent += "00000000"#顔アクセサリ
		datacontent += "00000000"#胸アクセサリ
		datacontent += "00000000"#上半身
		datacontent += "00000000"#下半身
		datacontent += "00000000"#背中
		datacontent += "00000000"#右手装備
		datacontent += "00000000"#左手装備
		datacontent += "00000000"#靴
		datacontent += "00000000"#靴下
		datacontent += "00000000"#ペット
		datacontent += "0d"#変わらないらしい----キャラ2
		datacontent += "00000000"#頭
		datacontent += "00000000"#頭アクセサリ
		datacontent += "00000000"#顔
		datacontent += "00000000"#顔アクセサリ
		datacontent += "00000000"#胸アクセサリ
		datacontent += "00000000"#上半身
		datacontent += "00000000"#下半身
		datacontent += "00000000"#背中
		datacontent += "00000000"#右手装備
		datacontent += "00000000"#左手装備
		datacontent += "00000000"#靴
		datacontent += "00000000"#靴下
		datacontent += "00000000"#ペット
		datacontent += "0d"#変わらないらしい----キャラ3
		datacontent += "00000000"#頭
		datacontent += "00000000"#頭アクセサリ
		datacontent += "00000000"#顔
		datacontent += "00000000"#顔アクセサリ
		datacontent += "00000000"#胸アクセサリ
		datacontent += "00000000"#上半身
		datacontent += "00000000"#下半身
		datacontent += "00000000"#背中
		datacontent += "00000000"#右手装備
		datacontent += "00000000"#左手装備
		datacontent += "00000000"#靴
		datacontent += "00000000"#靴下
		datacontent += "00000000"#ペット
		return datatype, datacontent
	
	def create00a8(self,pc,mapid):
		"""キャラクターマップ通知"""
		datatype = "00a8"#キャラクターマップ通知
		datacontent = self.pack(mapid, 8)#マップ
		#datacontent += "00000000"
		#datacontent += "00000000"
		#datacontent += "00000000"
		return datatype, datacontent
	
	def create0033(self, address, port, reply=False):
		"""接続先通知要求(ログインサーバ/0032)の応答"""
		datatype = "0033"
		if reply:
			datacontent = ""
		else:
			datacontent = "01"
			datacontent += self.packstr(address)
			datacontent += self.pack(port,8)
		return datatype, datacontent
	
	def create00dd(self):
		"""フレンドリスト(自キャラ)"""
		datatype = "00dd"#フレンドリスト(自キャラ)
		datacontent = "01"#現在の状態
		#0-12:オフライン、オンライン、募集中、取り込み中、
		#お話し中、休憩中、退席中、戦闘中、商売中、憑依中、
		#クエスト中、お祭り中、連絡求む
		datacontent += "01"+"00"#コメント
		return datatype, datacontent
	
	def create0032(self):
		"""接続確認(マップサーバ)"""#サーバ側では使えないらしい
		datatype = "0032"
		datacontent = ""
		return datatype, datacontent
	
	def create000f(self):
		"""マップサーバーのPASS鍵送信"""
		datatype = "000f"
		datacontent = "3030303030303030"
		return datatype, datacontent
	
	def create0011(self):
		"""認証結果(マップサーバーに認証情報の送信(s0010)に対する応答)"""
		datatype = "0011"
		datacontent = "00000000"
		datacontent += "0100"#tstr
		datacontent += "486eb420"#不明
		return datatype, datacontent
	
	def create1239(self,pc,speed):
		"""キャラ速度通知・変更"""
		datatype = "1239"
		datacontent = self.pack(pc.sid, 8) #サーバキャラID 
		datacontent += self.pack(speed, 4)#移動速度
		return datatype, datacontent
	
	def create1a5f(self):
		"""右クリ設定"""
		datatype = "1a5f"#右クリ設定
		datacontent = "00000000"
		return datatype,datacontent
	
	def create0203(self, pc, item, iid, part):
		"""インベントリ情報"""
		datatype = "0203"#アイテム欄のアイテムデータ
		datacontent = "00"#unknown#常に0
		datacontent += "d6"#データサイズ
		datacontent += self.pack(iid, 8)#インベントリNo
		datacontent += self.pack(item.id, 8)#アイテムID
		datacontent += "00000000"#見た目,フィギュア,スケッチ情報
		datacontent += self.pack(part, 2)#アイテムの場所
		datacontent += "00000001"#鑑定済み:0x01 カードロック？:0x20
		datacontent += self.pack(item.durability_max, 4)#耐久度
		datacontent += self.pack(item.durability_max, 4)#最大耐久度or最大親密度
		datacontent += "0000"#強化回数
		datacontent += "0000"#カードスロット数
		datacontent += "00000000"#カードID1
		datacontent += "00000000"#カードID2
		datacontent += "00000000"#カードID3
		datacontent += "00000000"#カードID4
		datacontent += "00000000"#カードID5
		datacontent += "00000000"#カードID6
		datacontent += "00000000"#カードID7
		datacontent += "00000000"#カードID8
		datacontent += "00000000"#カードID9
		datacontent += "00000000"#カードID10
		datacontent += "00"#染色
		datacontent += self.pack(item.count, 4)#個数
		datacontent += self.pack(item.price, 8)#ゴーレム販売価格
		datacontent += "0000"#ゴーレム販売個数
		datacontent += "0000"#憑依重量
		datacontent += "0000"#最大重量
		datacontent += "0000"#最大容量
		datacontent += "0000"#位置的に発動Skill？
		datacontent += "0000"#使用可能Skill
		datacontent += "0000"#位置的にパッシブスキル？
		datacontent += "0000"#位置的に憑依時可能Skill？
		datacontent += "0000"#位置的に憑依パッシブSkill？
		datacontent += self.pack(item.str, 4)#str
		datacontent += self.pack(item.mag, 4)#mag
		datacontent += self.pack(item.vit, 4)#vit
		datacontent += self.pack(item.dex, 4)#dex
		datacontent += self.pack(item.agi, 4)#agi
		datacontent += self.pack(item.int, 4)#int
		datacontent += self.pack(item.luk, 4)#luk （ペットの場合現在HP
		datacontent += self.pack(item.cha, 4)#cha（ペットの場合転生回数
		datacontent += self.pack(item.hp, 4)#HP（使用出来るアイテムは回復
		datacontent += self.pack(item.sp, 4)#SP（同上
		datacontent += self.pack(item.mp, 4)#MP（同上
		datacontent += self.pack(item.speed, 4)#移動速度
		datacontent += self.pack(item.atk1, 4)#物理攻撃力(叩)
		datacontent += self.pack(item.atk2, 4)#物理攻撃力(斬)
		datacontent += self.pack(item.atk3, 4)#物理攻撃力(突)
		datacontent += self.pack(item.matk, 4)#魔法攻撃力
		datacontent += self.pack(item.DEF, 4)#物理防御
		datacontent += self.pack(item.mdef, 4)#魔法防御
		datacontent += self.pack(item.s_hit, 4)#近命中力
		datacontent += self.pack(item.l_hit, 4)#遠命中力
		datacontent += self.pack(item.magic_hit, 4)#魔命中力
		datacontent += self.pack(item.s_avoid, 4)#近回避
		datacontent += self.pack(item.l_avoid, 4)#遠回避
		datacontent += self.pack(item.magic_avoid, 4)#魔回避
		datacontent += self.pack(item.critical_hit, 4)#クリティカル
		datacontent += self.pack(item.critical_avoid, 4)#クリティカル回避
		datacontent += self.pack(item.heal_hp, 4)#回復力？
		datacontent += self.pack(item.heal_mp, 4)#魔法回復力？
		datacontent += "0000"#スタミナ回復力？
		datacontent += self.pack(item.energy, 4)#無属性？
		datacontent += self.pack(item.fire, 4)#火属性
		datacontent += self.pack(item.water, 4)#水属性
		datacontent += self.pack(item.wind, 4)#風属性
		datacontent += self.pack(item.earth, 4)#地属性
		datacontent += self.pack(item.light, 4)#光属性
		datacontent += self.pack(item.dark, 4)#闇属性
		datacontent += self.pack(item.poison, 4)#毒（+なら毒回復、−なら毒状態に
		datacontent += self.pack(item.stone, 4)#石化
		datacontent += self.pack(item.paralyze, 4)#麻痺
		datacontent += self.pack(item.sleep, 4)#睡眠
		datacontent += self.pack(item.silence, 4)#沈黙
		datacontent += self.pack(item.slow, 4)#鈍足
		datacontent += self.pack(item.confuse, 4)#混乱
		datacontent += self.pack(item.freeze, 4)#凍結
		datacontent += self.pack(item.stan, 4)#気絶
		datacontent += "0000"#ペットステ（攻撃速度
		datacontent += "0000"#ペットステ（詠唱速度
		datacontent += "0000"#ペットステ？（スタミナ回復力？
		datacontent += self.pack(item.price, 8)#ゴーレム露店の買取価格
		datacontent += "0000"#ゴーレム露店の買取個数
		datacontent += self.pack(item.price, 8)#商人露店の販売価格
		datacontent += "0000"#商人露店の販売個数
		datacontent += "00000000"#何かの価格？ 商人露店の買取価格の予約？
		datacontent += "0000"#何かの個数？
		datacontent += "0001"#unknow
		datacontent += "01"#unknow
		datacontent += "0000"#unknow
		datacontent += "ffffffff"#unknow
		datacontent += "00"#unknow
		#while len(datacontent) < 432:
		#	datacontent += "00"
		return datatype, datacontent
	
	def create01ff(self, pc):
		"""自分のキャラクター情報"""
		datatype = "01ff"#自分のキャラクター情報
		datacontent = self.pack(pc.sid, 8)#サーバキャラID
		datacontent += self.pack(pc.charid, 8)#キャラID
		name = pc.name.encode("hex")+"00"
		namelength = str(int(len(name)/2))
		datacontent += self.pack(namelength, 2)+name#名前
		datacontent += self.pack(pc.race, 2)#種族
		datacontent += self.pack(pc.form, 2)#フォーム
		datacontent += self.pack(pc.gender, 2)#性別
		datacontent += self.pack(pc.hair, 4)#髪型
		datacontent += self.pack(pc.haircolor, 2)#髪色
		datacontent += self.pack(pc.wig, 4)#ウィング
		datacontent += "ff"#不明
		datacontent += self.pack(pc.face, 4)#顔
		datacontent += self.pack(pc.base_lv, 2)#転生前のレベル
		datacontent += self.pack(pc.ex, 2)#転生特典
		datacontent += self.pack(pc.wing, 2)#転生翼
		datacontent += self.pack(pc.wingcolor, 2)#転生翼色
		datacontent += self.pack(pc.map, 8)#マップ
		datacontent += self.pack(pc.x, 2)+self.pack(pc.y, 2)+self.pack(pc.dir, 2)#x y dir
		datacontent += "00000056"+"00000056"#hp+maxhp
		datacontent += "00000028"+"00000028"#mp+maxmp
		datacontent += "00000022"+"00000022"#sp+maxsp
		datacontent += "00000003"+"0000001e"#ep+maxep
		datacontent += "0009"#不明
		datacontent += "08"#ステータス数#常に0x08
		datacontent += self.pack(pc.str, 4)#str
		datacontent += self.pack(pc.dex, 4)#dex
		datacontent += self.pack(pc.int, 4)#int
		datacontent += self.pack(pc.vit, 4)#vit
		datacontent += self.pack(pc.agi, 4)#agi
		datacontent += self.pack(pc.mag, 4)#mag
		datacontent += "0000"#luk
		datacontent += "0000"#cha
		datacontent += "14"#equip_len？
		datacontent += "0000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "FFFFFFFF"#憑依対象サーバーキャラID
		datacontent += "00"#憑依場所 ( r177b等も参照
		datacontent += self.pack(pc.gold, 8)#所持金
		cachetype,cache = self.create09e9(pc)
		cache = cache[8:]
		datacontent += cache#装備の0Dから乗り物の染色値まで
		datacontent += "01"#不明
		datacontent += "00000000"#不明
		datacontent += "00000002"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#不明
		datacontent += "00000000"#unknow
		datacontent += "00000000"#unknow
		datacontent += "0001"#不明
		#while len(datacontent) < 600:
		#	datacontent += "00"
		return datatype, datacontent

	def create03f2(self, msgid):
		"""システムメッセージ"""
		datatype = "03f2"#システムメッセージ
		datacontent = self.pack(msgid, 4)
		return datatype, datacontent

	def create09ec(self, pc):
		"""ゴールドを更新する
		値は更新後の値"""
		datatype = "09ec"#ゴールド入手 
		datacontent = self.pack(pc.gold, 8)
		return datatype, datacontent

	def create0221(self, pc):
		"""最大HP/MP/SP"""
		datatype = "0221"#最大HP/MP/SP
		datacontent = self.pack(pc.charid, 8)#キャラID
		datacontent += "04"#hp mp sp epの4つ
		datacontent += self.pack(pc.status.maxhp, 8)#hp
		datacontent += self.pack(pc.status.maxmp, 8)#mp
		datacontent += self.pack(pc.status.maxsp, 8)#sp
		datacontent += self.pack(pc.status.maxep, 8)#ep
		return datatype, datacontent
	
	def create021c(self, pc, ismob=False):
		"""現在のHP/MP/SP/EP"""
		datatype = "021c"#最大HP/MP/SP
		datacontent = self.pack(pc.sid, 8) #サーバID(キャラIDではない)
		datacontent += "04"#hp mp sp epの4つ
		if ismob:
			datacontent += self.pack(pc.hp, 8) #hp
			datacontent += self.pack(pc.mp, 8) #mp
			datacontent += self.pack(pc.sp, 8) #sp
			datacontent += self.pack(pc.ep, 8) #ep
		else:
			datacontent += self.pack(pc.status.hp, 8) #hp
			datacontent += self.pack(pc.status.mp, 8) #mp
			datacontent += self.pack(pc.status.sp, 8) #sp
			datacontent += self.pack(pc.status.ep, 8) #ep
		return datatype, datacontent
	
	def create0212(self, pc):
		"""ステータス・補正・ボーナスポイント"""
		datatype = "0212"#ステータス・補正・ボーナスポイント
		datacontent = "08"#base
		datacontent += self.pack(pc.str, 4)#str
		datacontent += self.pack(pc.dex, 4)#dex
		datacontent += self.pack(pc.int, 4)#int
		datacontent += self.pack(pc.vit, 4)#vit
		datacontent += self.pack(pc.agi, 4)#agi
		datacontent += self.pack(pc.mag, 4)#mag
		datacontent += "0000"#luk
		datacontent += "0000"#cha
		datacontent += "08"#revise
		datacontent += self.pack(pc.stradd, 4)#str
		datacontent += self.pack(pc.dexadd, 4)#dex
		datacontent += self.pack(pc.intadd, 4)#int
		datacontent += self.pack(pc.vitadd, 4)#vit
		datacontent += self.pack(pc.agiadd, 4)#agi
		datacontent += self.pack(pc.magadd, 4)#mag
		datacontent += "0000"#luk
		datacontent += "0000"#cha
		datacontent += "08"#bounus
		datacontent += "0000"#str
		datacontent += "0000"#dex
		datacontent += "0000"#int
		datacontent += "0000"#vit
		datacontent += "0000"#agi
		datacontent += "0000"#mag
		datacontent += "0000"#luk
		datacontent += "0000"#cha
		return datatype, datacontent
	
	def create0217(self, pc):
		"""詳細ステータス"""
		datatype = "0217"#詳細ステータス
		datacontent = "1e"#30
		datacontent += self.pack(pc.status.speed, 4)#歩く速度
		datacontent += self.pack(pc.status.minatk1, 4)#最小ATK1
		datacontent += self.pack(int(pc.status.minatk2)+1, 4)#最小ATK2
		datacontent += self.pack(int(pc.status.minatk3)+3, 4)#最小ATK3
		datacontent += self.pack(pc.status.maxatk1, 4)#最大ATK1
		datacontent += self.pack(int(pc.status.maxatk2)+1, 4)#最大ATK2
		datacontent += self.pack(int(pc.status.maxatk3)+3, 4)#最大ATK3
		datacontent += self.pack(pc.status.minmatk, 4)#最小MATK
		datacontent += self.pack(pc.status.maxmatk, 4)#最大MATK
		datacontent += self.pack(pc.status.leftdef, 4)#基本DEF
		datacontent += self.pack(pc.status.rightdef, 4)#追加DEF
		datacontent += self.pack(pc.status.leftmdef, 4)#基本MDEF
		datacontent += self.pack(pc.status.rightmdef, 4)#追加MDEF
		datacontent += self.pack(pc.status.shit, 4)#S.HIT(近距離命中率)
		datacontent += self.pack(pc.status.lhit, 4)#L.HIT(遠距離命中率)
		datacontent += self.pack(pc.status.mhit, 4)#魔法命中
		datacontent += self.pack(pc.status.chit, 4)#クリティカル命中
		datacontent += self.pack(pc.status.savoid, 4)#S.AVOID(近距離回避力)
		datacontent += self.pack(pc.status.lavoid, 4)#L.AVOID(遠距離回避力)
		datacontent += "0000"#魔法回避力
		datacontent += self.pack(pc.status.hpheal,4)#HP回復率
		datacontent += self.pack(pc.status.mpheal,4)#MP回復率
		datacontent += self.pack(pc.status.spheal,4)#SP回復率
		datacontent += "0000"#不明
		datacontent += self.pack(pc.status.aspd,4)#A.SPD(攻撃速度)
		datacontent += self.pack(pc.status.cspd,4)#C.SPD(詠唱速度)
		datacontent += "0000"#不明
		datacontent += "0000"#不明
		datacontent += "0000"#不明
		datacontent += "0000"#不明
		return datatype, datacontent
	
	def create0259(self, pc):
		"""ステータス試算結果"""
		datatype = "0259"#詳細ステータス
		cachetype, cache = self.create0217(pc)
		datacontent = cache
		datacontent += "03"#03固定#次のdwordの数？
		datacontent += self.pack(pc.status.maxhp, 8)#最大hp
		datacontent += self.pack(pc.status.maxmp, 8)#最大mp
		datacontent += self.pack(pc.status.maxsp, 8)#最大sp
		datacontent += self.pack(pc.status.maxcapa, 4)#最大Capa
		datacontent += self.pack(pc.status.maxpayl, 4)#最大payload
		return datatype, datacontent
	
	def create0230(self, pc):
		"""現在CAPA/PAYL"""
		datatype = "0230"#現在CAPA/PAYL
		datacontent = "04"
		datacontent += self.pack(pc.status.capa, 8)#CAPA(x0.1)
		datacontent += self.pack(pc.status.rightcapa, 8)#右手かばんCAPA(x0.1)
		datacontent += self.pack(pc.status.leftcapa, 8)#左手かばんCAPA(x0.1)
		datacontent += self.pack(pc.status.backcapa, 8)#背中CAPA(x0.1)
		datacontent += "04"
		datacontent += self.pack(pc.status.payl, 8)#PAYL(x0.1)
		datacontent += self.pack(pc.status.rightpayl, 8)#右手かばんPAYL(x0.1)
		datacontent += self.pack(pc.status.leftpayl, 8)#左手かばんPAYL(x0.1)
		datacontent += self.pack(pc.status.backpayl, 8)#背中PAYL(x0.1)
		return datatype, datacontent
	
	def create0231(self, pc):
		"""最大CAPA/PAYL"""
		datatype = "0231"#最大CAPA/PAYL
		datacontent = "04"
		datacontent += self.pack(pc.status.maxcapa, 8)#CAPA(x0.1)
		datacontent += self.pack(pc.status.maxrightcapa, 8)#右手かばんCAPA(x0.1)
		datacontent += self.pack(pc.status.maxleftcapa, 8)#左手かばんCAPA(x0.1)
		datacontent += self.pack(pc.status.maxbackcapa, 8)#背中CAPA(x0.1)
		datacontent += "04"
		datacontent += self.pack(pc.status.maxpayl, 8)#PAYL(x0.1)
		datacontent += self.pack(pc.status.maxrightpayl, 8)#右手かばんPAYL(x0.1)
		datacontent += self.pack(pc.status.maxleftpayl, 8)#左手かばんPAYL(x0.1)
		datacontent += self.pack(pc.status.maxbackpayl, 8)#背中PAYL(x0.1)
		return datatype, datacontent
	
	def create0244(self, pc):
		"""職業"""
		datatype = "0244"#職業
		datacontent = self.pack(pc.job, 8)#職業ID
		datacontent += "00000000"#ジョイントジョブID
		return datatype, datacontent
	
	def create0226(self, pc, num):
		"""スキル一覧"""
		datatype = "0226"#スキル一覧
		if int(num) == 0: #一次職
			skillcount = len(pc.skill_list)
		else:
			skillcount = 0
		datacontent = self.pack(skillcount, 2) #スキルIDの数
		if int(num) == 0:
			for i in pc.skill_list:
				datacontent += self.pack(i, 4) #スキルID
		datacontent += self.pack(skillcount, 2) #習得Lvの数
		for i in pc.skill_list:
			s = self.skilldic.get(i)
			if not s:
				datacontent += self.pack(1, 2) #習得Lv #暫くlv1に固定
			else:
				datacontent += self.pack(s.maxlv, 2) #習得Lv #暫くmaxlvに固定
		datacontent += self.pack(skillcount, 2) #不明
		for i in xrange(skillcount):
			datacontent += self.pack(0, 2) #不明
		datacontent += self.pack(skillcount, 2) #習得可能Lvの数
		for i in xrange(skillcount):
			datacontent += self.pack(1, 2) #習得可能LvLv #暫くlv1に固定
		datacontent += self.pack(num, 2) #一次職なら0 エキスパ1 etc...
		datacontent += self.pack(skillcount, 2) #習得スキル数 #TODO#レベル０のスキルを計算から外す
		return datatype, datacontent
	
	def create022e(self, pc):
		"""リザーブスキル"""
		datatype = "022e"#リザーブスキル
		datacontent = "0000"
		return datatype, datacontent
	
	def create023a(self, pc):
		"""Lv JobLv ボーナスポイント スキルポイント"""
		datatype = "023a"#Lv JobLv ボーナスポイント スキルポイント
		datacontent = self.pack(pc.lv_base, 2)#Lv
		datacontent += self.pack(pc.lv_job1, 2)#JobLv(1次職)
		datacontent += self.pack(pc.lv_job2x, 2)#JobLv(エキスパート)
		datacontent += self.pack(pc.lv_job2t, 2)#JobLv(テクニカル)
		datacontent += self.pack(pc.lv_job3, 2)#三次職のレベル？
		datacontent += "01"#JobLv(ジョイント？ブリーダー？)
		datacontent += "0002"#ボーナスポイント
		datacontent += "0003"#スキルポイント(1次職)
		datacontent += "0000"#スキルポイント(エキスパート)
		datacontent += "0000"#スキルポイント(テクニカル)
		datacontent += "0000"#三次職のポイント？
		return datatype, datacontent
	
	def create0235(self, pc):
		"""EXP/JOBEXP"""
		datatype = "0235"#EXP/JOBEXP
		datacontent = "00000000"#EXP(x0.1%)
		datacontent += "00000000"#JobEXP(x0.1%)
		datacontent += "00000000"#WarRecodePoint 
		datacontent += "00000000"#ecoin
		datacontent += "00000000"+"00000000"#baseexp
		datacontent += "00000000"+"00000000"#jobexp
		return datatype, datacontent
	
	def create09e9(self, pc):
		"""装備情報#IDのキャラの見た目を変更"""
		datatype = "09e9"#装備情報#IDのキャラの見た目を変更
		datacontent = self.pack(pc.charid, 8)#キャラID
		datacontent += "0d"#装備の数(常に0x0D)#13
		item = pc.item.get(pc.equip.head)
		#頭
		if item != None and item.type == "HELM":
			datacontent += self.pack(pc.item[pc.equip.head].id, 8)
		else:
			datacontent += "00000000"
		#頭アクセサリ
		if item != None and item.type == "ACCESORY_HEAD":
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		item = pc.item.get(pc.equip.face)
		#顔
		if item != None and item.type == "FULLFACE":
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#顔アクセサリ
		if item != None and item.type == "ACCESORY_FACE":
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		item = pc.item.get(pc.equip.chestacce)
		#胸アクセサリ
		if item != None and item.type in ACCESORY_TYPE_LIST:
				datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		item = pc.item.get(pc.equip.tops)
		#上半身+下半身
		if item != None and item.type == "ONEPIECE":
			datacontent += self.pack(item.id, 8)
			datacontent += "00000000"
		else:
			if item != None and item.type in UPPER_TYPE_LIST:
				datacontent += self.pack(item.id, 8)
			else:
				datacontent += "00000000"
			item = pc.item.get(pc.equip.bottoms)
			if item != None and item.type in LOWER_TYPE_LIST:
				datacontent += self.pack(item.id, 8)
			else:
				datacontent += "00000000"
		#背中
		item = pc.item.get(pc.equip.backpack)
		if item != None and item.type == "BACKPACK":
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#右手装備
		item = pc.item.get(pc.equip.right)
		if item != None and item.type in RIGHT_TYPE_LIST:
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#左手装備
		item = pc.item.get(pc.equip.left)
		if item != None and item.type in LEFT_TYPE_LIST:
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#靴
		item = pc.item.get(pc.equip.shoes)
		if item != None and item.type in BOOTS_TYPE_LIST:
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#靴下
		item = pc.item.get(pc.equip.socks)
		if item != None and item.type == "SOCKS":
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		#ペット
		item = pc.item.get(pc.equip.pet)
		if item != None and item.type in PET_TYPE_LIST:
			datacontent += self.pack(item.id, 8)
		else:
			datacontent += "00000000"
		datacontent += "03"+"000000"#左手モーションタイプ size=3 { 片手, 両手, 攻撃}
		datacontent += "03"+"000000"#右手モーションタイプ size=3
													# chr_act_tbl.csvを参照する
		datacontent += "03"+"000000"#乗り物モーションタイプ size=3
		datacontent += "00000000"#乗り物アイテムID
		datacontent += "00"#乗り物の染色値
		datacontent += "00"#戦闘状態の時1#0fa6で変更要請#0fa7で変更される
		return datatype, datacontent
	
	def create196e(self, pc):
		"""クエスト回数・時間"""
		datatype = "196e"#クエスト回数・時間
		datacontent = "0003"#残り数
		datacontent += "00000001"#何時間後に3追加されるか
		datacontent += "00000000"#不明#常に0？
		return datatype,datacontent
	
	def create1b67(self):
		"""マップ情報完了通知
		MAPログイン時に基本情報を全て受信した後に受信される"""
		datatype = "1b67"#マップ情報完了通知
		datacontent = "00000000" #unknow
		datacontent = "00" #unknow
		return datatype, datacontent
	
	def create0fa6(self, pc, battlestatus):
		"""戦闘状態変更通知"""
		datatype = "0fa6"#戦闘状態変更通知
		datacontent = self.pack(pc.sid, 8) #サーバキャラID
		datacontent += self.pack(battlestatus, 2) #00: 通常状態 01: 戦闘状態
		return datatype, datacontent
	
	def create05dc(self):
		"""イベント開始の通知"""
		datatype = "05dc"#イベント開始の通知
		datacontent = ""
		return datatype,datacontent

	def create05e8(self, eventid):
		"""EventID通知。 Event送信に対する応答"""
		datatype = "05e8"#EventID通知。 Event送信に対する応答
		datacontent = self.pack(eventid, 8)+"00000000"
		return datatype, datacontent

	def create05dd(self):
		"""イベント終了の通知"""
		datatype = "05dd"#イベント終了の通知
		datacontent = ""
		return datatype, datacontent

	def create09d4(self, pc, item, iid, part):
		"""アイテム取得"""
		datatype = "09d4"#アイテム取得
		cachetype,cache = self.create0203(pc, item, iid, part)
		datacontent = cache[2:]#先頭のunknownを除く
		datacontent += "00"
		return datatype, datacontent

	def create09ce(self, iid):
		"""インベントリからアイテム消去"""
		datatype = "09ce"#インベントリからアイテム消去
		datacontent = self.pack(iid,8)#インベントリID
		return datatype, datacontent
	
	def create03e9(self, text, sid):
		"""オープンチャット・システムメッセージ"""
		datatype = "03e9"
		text = text.encode("hex")+"00"
		textlength = len(text) / 2 #len(text.decode("hex"))
		datacontent = self.pack(sid, 8)#発言者ID
		datacontent += self.pack(textlength, 2)+text
		#発言者ID
		#* -1 : システムメッセージ(黄)
		#* 0 : 管理者メッセージ(桃)
		#* 1-9999 : PCユーザー
		#* 10000-30000 : ペット
		#* 他 : 飛空庭設置ペットなど
		return datatype, datacontent
	
	def create121c(self, pc, motionid, isloop=0, object_id=None):
		"""モーション通知"""
		if not object_id:
			object_id = pc.sid
		datatype = "121c"#モーション通知
		datacontent = self.pack(object_id, 8)#サーバキャラID
		datacontent += self.pack(motionid, 4)#モーションID
		datacontent += self.pack(isloop, 2)#ループさせるかどうか
		datacontent += "00"#不明
		return datatype, datacontent
	
	def create09e3(self, iid, part):
		"""アイテム保管場所変更"""
		datatype = "09e3"#アイテム保管場所変更
		datacontent = self.pack(iid, 8)#移動元インベントリID
		datacontent += "00"#成功時は0
		datacontent += self.pack(part, 2)#移動先保管場所(エラー時は-1
		return datatype, datacontent
	
	def create09e8(self, iid, part, result, r):
		"""アイテム装備"""
		datatype = "09e8"#アイテム装備
		datacontent = self.pack(iid, 8)#インベントリID, 装備をはずしたときは-1
		datacontent += self.pack(part, 2)#アイテムの装備先, 装備をはずしたときは-1
		datacontent += self.pack(result, 2)#通常0, noやpartが-1のとき1
		datacontent += self.pack(r, 8)#射程
		return datatype, datacontent
	
	def create020e(self, pc):
		"""キャラ情報"""
		datatype = "020e"#キャラ情報
		datacontent = self.pack(pc.sid, 8)#サーバキャラID
		datacontent += self.pack(pc.charid, 8)#固有ID
		name = pc.name.encode("hex")+"00"
		namelength = str(int(len(name)/2))
		datacontent += self.pack(namelength, 2)#名前の長さ
		datacontent += name#名前
		datacontent += self.pack(pc.race, 2)#種族
		datacontent += self.pack(pc.form, 2)#フォーム
		datacontent += self.pack(pc.gender, 2)#性別
		datacontent += self.pack(pc.hair, 4)#髪型
		datacontent += self.pack(pc.haircolor, 2)#髪色
		datacontent += self.pack(pc.wig, 4)#ウィング
		datacontent += "ff"#不明
		datacontent += self.pack(pc.face, 4)#顔
		datacontent += self.pack(pc.base_lv, 2)#転生前のレベル
		datacontent += self.pack(pc.ex, 2)#転生特典
		datacontent += self.pack(pc.wing, 2)#転生翼
		datacontent += self.pack(pc.wingcolor, 2)#転生翼色
		cachetype, cache = self.create09e9(pc)
		cache = cache[8:]
		datacontent += cache#装備の0Dから乗り物の染色値まで
		datacontent += "01"+"00"#パーティー名
		datacontent += "01"#パーティーリーダーor未所属なら1、それ以外は0
		datacontent += "00000000"#リングID#変更時はr1ad1
		datacontent += "01"+"00"#リング名
		datacontent += "01"#1:リンマスorリングに入ってない 0:リングメンバ
		datacontent += "01"+"00"#看板
		datacontent += "01"+"00"#露店看板
		datacontent += "00"#プレイヤー露店かどうか
		datacontent += self.pack("1000", 8)#chara size (1000が標準
		datacontent += self.pack(pc.motion, 4)#モーション#ただし座り(135)や移動や
										#武器・騎乗ペットによるモーションの場合0
		datacontent += "00000000"#不明
		datacontent += "00000002"#2 r0fa7参照
		datacontent += "00000000"#0 r0fa7参照
		datacontent += "00"#演習時のエンブレムとか#1東2西4南8北Aヒーロー状態
		datacontent += "00"#メタモーバトルのチーム#1花2岩
		datacontent += "00"#1にすると/joyのモーションを取る
								#（マリオネット変身時。）2にすると〜
		datacontent += "00"#不明
		datacontent += "00"#ゲストIDかどうか
		datacontent += self.pack(pc.lv_base, 2)#レベル（ペットは1固定
		datacontent += "00000000"#WRP順位（ペットは -1固定。
								#別のパケで主人の値が送られてくる
		datacontent += "00000000"#不明
		datacontent += "FF"#不明
		return datatype, datacontent
	
	def create11f9(self, pc, movetype=7):
		"""キャラ移動アナウンス"""
		datatype = "11f9"#キャラの移動
		datacontent = self.pack(pc.sid, 8) #server id
		datacontent += self.pack(pc.rawx, 4) #raw x
		datacontent += self.pack(pc.rawy, 4) #raw y
		datacontent += self.pack(pc.rawdir, 4) #raw dir
		datacontent += self.pack(movetype, 4) #type
		#type
		#	1	向き変更のみ
		#	6	歩き
		#	7	走り
		#	8	強制移動(ノックバック) (グローブ等)
		#	14	ワープ(ソーサラースキル・テレポート等)
		return datatype, datacontent
	
	def create120c(self, pc):
		"""他キャラ情報/他キャラの憑依やHP等の情報"""
		datatype = "120c"#他キャラの移動
		datacontent = self.pack(pc.sid, 8)#サーバキャラID
		datacontent += self.pack(pc.x, 2)#x
		datacontent += self.pack(pc.y, 2)#y
		datacontent += self.pack(pc.status.speed, 4)#キャラの足の早さ
		datacontent += self.pack(pc.dir, 2)#向き
		datacontent += "ffffffff"#憑依先のキャラID。（未憑依時:0xFFFFFFFF
		datacontent += "ff"#憑依箇所。(0:右手 1:左手 2:胸 3:鎧) (未憑依:FF)
		datacontent += self.pack(pc.status.hp, 8)#現在HP
		datacontent += self.pack(pc.status.maxhp, 8)#最大HP
		return datatype, datacontent
	
	def create03f8(self):
		"""NPCメッセージのヘッダー"""
		datatype = "03f8"#NPCメッセージのヘッダー
		datacontent = ""
		return datatype, datacontent
	
	def create03f9(self):
		"""NPCメッセージのフッター"""
		datatype = "03f9"#NPCメッセージのフッター
		datacontent = ""
		return datatype, datacontent
	
	def create03f7(self, pc, text, npc_name, motion_id=131, npcid=None):
		"""#NPCメッセージ"""
		if not npcid:
			npcid = pc.e.id
		datatype = "03f7"#NPCメッセージ
		npc_name = npc_name.encode("hex")
		if len(npc_name) > 508:
			npc_name = npc_name[:508]#508 + 2 = 255 * 2
		npc_name = npc_name+"00"
		npc_name_length = len(npc_name) / 2
		text = text.encode("hex")
		if len(text) > 504:
			text = text[:504]#504 + 6 = 255 * 2
		text = text+"2452"+"00"#2452 = $R
		text_length = len(text) / 2
		datacontent = self.pack(npcid, 8)
		datacontent += "00" #unknow
		datacontent += "01" #isnpcexist
		datacontent += self.pack(text_length, 2)+text
		datacontent += self.pack(motion_id, 4)
		datacontent += self.pack(npc_name_length, 2)+npc_name
		return datatype, datacontent
	
	def create11fd(self, pc, mapid, x, y):
		"""マップ変更通知 """
		datatype = "11fd"#マップ変更通知 
		datacontent = self.pack(mapid, 8)#mapid
		datacontent += self.pack(x, 2)#x
		datacontent += self.pack(y, 2)#y
		#datacontent += self.pack(pc.dir,2)#dir
		datacontent += "00"#dir
		datacontent += "04"#常に0x04
		datacontent += "FF"#常に0xff#インスDにおける移動後の部屋の位置x
		datacontent += "FF"#常に0xff#インスDにおける移動後の部屋の位置y
		datacontent += "00"#motion
		datacontent += "00000000"#大体0#値が入ってるときはかなり大きめの値
		return datatype, datacontent
	
	def create1211(self, pc):
		"""PC消去"""
		datatype = "1211"#マップ変更通知 
		datacontent = self.pack(pc.sid, 8) #サーバキャラID
		return datatype,datacontent
	
	def create09cf(self, iid, count):
		"""アイテム個数変化"""
		datatype = "09cf"#インベントリ内のアイテムの個数を増減させる
		datacontent = self.pack(iid, 8)#インベントリID
		datacontent += self.pack(count, 4)#変化後の個数
		return datatype, datacontent
	
	def create0606(self):
		"""s0605で選択結果が通知された場合の応答
		箱を開けた場合は返答しない"""
		datatype = "0606"#s0605で選択結果が通知された場合の応答
		datacontent = "00"#常に0
		return datatype, datacontent
	
	def create0604(self, optionlist, title=""):
		"""NPCのメッセージのうち、選択肢から選ぶもの
		選択結果はs0605で通知する"""
		optioncount = str(len(optionlist))
		datatype = "0604"#NPCメッセージ(選択肢) 
		datacontent = self.packstr(title)#ウィンドウタイトル('\0'あり)
		datacontent += self.pack(optioncount, 2)#選択肢の数 65以上でエラー
		for x in optionlist:
			datacontent += self.packstr(x)
			#選択肢('\0'なし)
		datacontent += "0100"#選んだときに確認するメッセージのタイトル
		datacontent += "00"#キャンセルできるかどうか
		datacontent += "00000000"
		#timeout秒に選ばないとキャンセルしたことになる。0の場合制限無し
		return datatype, datacontent
	
	def create0613(self, pc, itemidlist, magnification=100):
		"""NPCのショップウィンドウ"""
		datatype = "0613"#NPCのショップウィンドウ
		datacontent = self.pack(magnification, 8)#アイテムの販売価格の倍率(単位%)(100で標準)
		datacontent += self.pack(len(itemidlist), 2)#個数
		for x in itemidlist:
			datacontent += self.pack(x, 8)
		#アイテムID（13個以上はエラー
		datacontent += self.pack(pc.gold, 8)#所持金
		datacontent += "00000000"#銀行に預けてる金
		datacontent += "00"#0普通の店1CPの店2ecoin
		return datatype, datacontent
	
	def create0a19(self, pc):
		"""自分・相手がOKやキャンセルを押した際に双方に送信される"""
		datatype = "0a19"#相手のOKやキャンセル状態?
		datacontent = self.pack(pc.tradestate, 2)#state1#自分と相手分? 常に2?
		datacontent += "00"#state2#自分と相手分? 常に2?
		#state1
		#00:OK押してない状態?
		#FF:OK押した状態?
		#01:トレード完了してる状態?
		#state2
		#00:OK押してない状態?
		#FF:OK押した状態?
		return datatype, datacontent
	
	def create0a1c(self, pc, isnpc=1, npcname=""):
		"""トレード終了通知
		トレードが成立・キャンセルされた場合などに受信"""
		datatype = "0a1c"#トレード終了通知
		datacontent = ""#無し
		return datatype, datacontent
	
	def create0a0f(self, pc, isnpc=1, npcname=""):
		"""トレードウィンドウ表示"""
		datatype = "0a0f"#トレードウィンドウ表示
		datacontent = self.packstr(npcname)#相手の名前
		datacontent += self.pack(isnpc, 8)#00だと人間? 01だとNPC?
		return datatype, datacontent
	
	def create05eb(self, time):
		"""イベント関連のウェイト"""
		datatype = "05eb"#イベント関連のウェイト
		datacontent = self.pack(time, 8)#ミリセカンド
		return datatype, datacontent
	
	def create0615(self, pc):
		"""NPCショップウィンドウ（売却）"""
		datatype = "0615"#NPCショップウィンドウ（売却）
		datacontent = "0000000a"#不明
		datacontent += "00000fa0"#不明
		datacontent += "00000000"#不明
		datacontent += "02"+"ffffffff"+"0cfb7fff"#不明
		return datatype, datacontent
	
	def create09f6(self, pc, warehouse_id, num_here, num_all, num_max):
		"""倉庫インベントリーヘッダ"""
		datatype = "09f6"#倉庫インベントリーヘッダ
		datacontent = self.pack(warehouse_id, 8)#倉庫の場所
		datacontent += self.pack(num_here, 8)#開いている倉庫にあるインベントリ数
		datacontent += self.pack(num_all, 8)#すべての倉庫にあるインベントリ数
		datacontent += self.pack(num_max, 8)#倉庫に入る最大インベントリ数
		#GAME_WARE_NAME_0,";アクロポリスシティ";
		#GAME_WARE_NAME_1,";ファーイースト国境駐在員";
		#GAME_WARE_NAME_2,";アイアンサウス国境駐在員";
		#GAME_WARE_NAME_3,";ノーザン国境駐在員";
		#GAME_WARE_NAME_4,";廃炭鉱キャンプ	";
		#GAME_WARE_NAME_5,";モーグシティ";
		#GAME_WARE_NAME_6,";アイアンサウス連邦";
		#GAME_WARE_NAME_7,";ノーザン王国";
		#GAME_WARE_NAME_8,";トンカシティ";
		#GAME_WARE_NAME_9,";";
		#GAME_WARE_NAME_10,";";
		#GAME_WARE_NAME_11,";";
		#GAME_WARE_NAME_12,";ファーイースト共和国";"""
		return datatype, datacontent
	
	def create09f9(self, pc, item, iid, part):
		"""倉庫インベントリーデータ"""
		datatype = "09f9"#倉庫インベントリーデータ
		cachetype,cache = self.create0203(pc, item, iid, part)
		#partが30(0x1e)の場合は開いた倉庫に、0の場合は別の倉庫にある。
		datacontent = cache[2:]#先頭のunknownを除く
		datacontent += "00"
		return datatype, datacontent
	
	def create09fa(self):
		"""倉庫インベントリーフッタ"""
		datatype = "09fa"#倉庫インベントリーフッタ
		datacontent = ""
		return datatype, datacontent
	
	def create09fc(self, result):
		"""倉庫から取り出した時の結果"""
		datatype = "09fc"#倉庫から取り出した時の結果 
		datacontent = self.pack(result, 8)
		#0
		#成功
		#-1〜-8
		#GAME_SMSG_WAREHOUSE_ERR1,";倉庫を開けていません";
		#GAME_SMSG_WAREHOUSE_ERR2,";指定されたアイテムは存在しません";
		#GAME_SMSG_WAREHOUSE_ERR3,";指定された数量が不正です";
		#GAME_SMSG_WAREHOUSE_ERR4,";倉庫のアイテム数が上限を超えてしまうためキャンセルされました";
		#GAME_SMSG_WAREHOUSE_ERR5,";キャラのアイテム数が100個を超えてしまうためキャンセルされました";
		#GAME_SMSG_WAREHOUSE_ERR6,";イベントアイテムは預けられません";
		#GAME_SMSG_WAREHOUSE_ERR7,";指定した格納場所は使用できません";
		#GAME_SMSG_WAREHOUSE_ERR8,";変身中のマリオネットは預ける事ができません";
		#それ以外
		#GAME_SMSG_WAREHOUSE_ERR99,";倉庫移動に失敗しました";
		return datatype, datacontent
	
	def create09fe(self, result):
		"""倉庫に預けた時の結果"""
		datatype = "09fe"#倉庫に預けた時の結果
		datacontent = self.pack(result, 8)
		#0
		#成功
		#-1〜-8
		#GAME_SMSG_WAREHOUSE_ERR1,";倉庫を開けていません";
		#GAME_SMSG_WAREHOUSE_ERR2,";指定されたアイテムは存在しません";
		#GAME_SMSG_WAREHOUSE_ERR3,";指定された数量が不正です";
		#GAME_SMSG_WAREHOUSE_ERR4,";倉庫のアイテム数が上限を超えてしまうためキャンセルされました";
		#GAME_SMSG_WAREHOUSE_ERR5,";キャラのアイテム数が100個を超えてしまうためキャンセルされました";
		#GAME_SMSG_WAREHOUSE_ERR6,";イベントアイテムは預けられません";
		#GAME_SMSG_WAREHOUSE_ERR7,";指定した格納場所は使用できません";
		#GAME_SMSG_WAREHOUSE_ERR8,";変身中のマリオネットは預ける事ができません";
		#それ以外
		#GAME_SMSG_WAREHOUSE_ERR99,";倉庫移動に失敗しました";
		return datatype, datacontent
	
	def create0a08(self, result):
		"""搬送結果(たぶん"""
		datatype = "0a08"#搬送結果(たぶん
		datacontent = self.pack(result, 8)
		#0
		#GAME_SMSG_TRANSPORT_ERR0,";アイテムを搬送しました";
		#-1〜-4
		#GAME_SMSG_TRANSPORT_ERR1,";倉庫を開けていません";
		#GAME_SMSG_TRANSPORT_ERR2,";指定されたアイテムは存在しません";
		#GAME_SMSG_TRANSPORT_ERR3,";指定された数量が不正です";
		#GAME_SMSG_TRANSPORT_ERR4,";倉庫のアイテム数が上限を超えてしまうためキャンセルされました";
		return datatype, datacontent
	
	def create05f0(self, sound_id, loop=1, volume=100):
		"""音楽を再生する"""
		datatype = "05f0"#音楽を再生する
		datacontent = self.pack(sound_id, 8)#MusicID#play(";data/sound/bgm_%d.wma";)
		datacontent += self.pack(loop, 2)#ループさせるかどうか
		datacontent += "00"#00固定
		datacontent += self.pack(volume, 8)#音量 (100がMax)
		return datatype, datacontent
	
	def create05f5(self, sound_id, loop=0, volume=100, balance=50):
		"""効果音を再生する"""
		datatype = "05f5"#効果音を再生する
		datacontent = self.pack(sound_id, 8)#SoundID#play(";data/sound/se_%d.wav";)
		datacontent += self.pack(loop, 2)#ループさせるかどうか
		datacontent += "00"#00固定
		datacontent += self.pack(volume, 8)#音量 (100がMax)
		datacontent += self.pack(balance, 2)#バランス(0で左から50で中央100で右から)
		return datatype, datacontent
	
	def create05fa(self, sound_id, loop=0, volume=100, balance=50):
		"""ジングルを再生する"""
		datatype = "05fa"#ジングルを再生する
		datacontent = self.pack(sound_id, 8)#SoundID#play(";data/sound/jin_%d.wav";)
		datacontent += self.pack(loop, 2)#ループさせるかどうか
		datacontent += "00"#00固定
		datacontent += self.pack(volume, 8)#音量 (100がMax)
		datacontent += self.pack(balance, 2)#バランス(0で左から50で中央100で右から)
		return datatype, datacontent
	
	def create060e(self, pc, effectid=0, sid=0, x=0, y=0, dir=0):
		"""エフェクト受信"""
		if not sid:
			sid = pc.sid
		if not x:
			x = pc.x
		if not y:
			y = pc.y
		if not dir:
			dir = pc.dir
		datatype = "060e"#指定されたキャラにエフェクトをかける
		datacontent = self.pack(sid, 8)#キャラID
		datacontent += self.pack(effectid, 8)#エフェクトID(EFFECT.dat&attr.dat
		datacontent += self.pack(x, 2)#x#自キャラにエフェクトが掛かった場合は0
		datacontent += self.pack(y, 2)#y#自キャラにエフェクトが掛かった場合は0
		datacontent += self.pack(dir, 2)#dir
		return datatype, datacontent
	
	def create1220(self, pc, newmob):
		"""モンスター情報"""
		datatype = "1220"#モンスターの情報
		datacontent = self.pack(newmob.sid, 8) #server id
		datacontent += self.pack(newmob.id, 8) #mobid
		datacontent += self.pack(newmob.x, 2) #x
		datacontent += self.pack(newmob.y, 2) #y
		datacontent += self.pack(newmob.speed, 4) #speed
		datacontent += self.pack(newmob.dir, 2) #dir
		datacontent += self.pack(newmob.hp, 8) #hp
		datacontent += self.pack(newmob.maxhp, 8) #maxhp
		return datatype, datacontent
	
	def create122a(self, pc=None, mobidlist=None, npc=False):
		"""モンスターID通知""" #before login and after map load and add mob
		datatype = "122a" #モンスターID通知
		if npc or pc==None:
			datacontent = "00" #0 or 0x28 #npcの場合は0？
		else:
			datacontent = "28" #0 or 0x28 # 0x28 = 40
			for x in mobidlist:
				datacontent += self.pack(x, 8) #mobid 1
			datacontent += "00000000" * 39 # 40 - 1
		return datatype, datacontent
	
	def create0fa1(self, source, target, atype=0, damage=1, flag=1):
		"""攻撃結果"""
		datatype = "0fa1" #s0f9fに対する応答 #その場にいるPCすべてに送られる
		datacontent = self.pack(source.sid, 8) #source server id
		datacontent += self.pack(target.sid, 8) #target server id
		datacontent += self.pack(atype, 2) #攻撃の種類
		datacontent += self.pack(damage, 8) #hp damage(回復の場合はマイナス
		datacontent += "00000000" #mp damage
		datacontent += "00000000" #sp damage
		datacontent += self.pack(flag, 8) #color_flag
		#アイテム使用やスキル使用結果のHP・MP・SPの色やエフェクト
		datacontent += "000007d0" #delay
		#行動できるようになるまでの長さ(＝モーションの長さ) 2000が標準 ASPDにより短くなる 単位 0.1% ?
		datacontent += "000007d0" #unknow
		#delayと同値? delayはDC等で短くなってもこの値は元のまま
		return datatype, datacontent
	
	def create1225(self, sid):
		"""モンスター消去"""
	 	datatype = "1225" #delete mob view
		datacontent = self.pack(sid, 8) #mob server id
		return datatype, datacontent
	
	def create00ca(self, target):
		"""ウィスパー失敗"""
		datatype = "00ca" # ウィスパーで送信先が見つからない
		datacontent = "ffffffff" # -1
		datacontent += self.packstr(target) # 対象
		return datatype, datacontent
	
	def create00ce(self, source, message):
		"""ウィスパー受信"""
		datatype = "00ce" # ウィスパーチャットの受信
		datacontent = self.packstr(source) # 送信者名前
		datacontent += self.packstr(message) # メッセージ
		return datatype, datacontent
	
	def create0fa7(self, pc, mode=02):
		"""キャラのモード変更""" #before map load
		datatype = "0fa7" #キャラのモード変更
		datacontent = self.pack(pc.sid, 8) #サーバキャラID 
		datacontent += self.pack(mode, 8) #通常 00000002
		datacontent += "00000000" #通常 00000000
		return datatype, datacontent
	
	def create1f72(self, show=False):
		"""もてなしタイニーアイコン""" #before login
		datatype = "1f72" #もてなしタイニーアイコンの表示非表示
		if show:
			datacontent = "01" #0非表示1表示 
		else:
			datacontent = "00" #0非表示1表示 
		return datatype, datacontent
	
	def create157c(self, pc, state01=0, state02=0, \
				state03=0, state04=0, state05=0, state06=0, \
				state07=0, state08=0, state09=0):
		"""キャラの状態""" #before login and after map load
		datatype = "157c"
		#キャラの自然回復や状態異常等、様々な状態を更新する
		#状態に応じて画面上にアイコンが出る
		#毒などの場合エフェクトも出る
		datacontent = self.pack(pc.sid, 8) #サーバキャラID
		#DWORD chara_id; DWORD state[9];
		datacontent += self.pack(state01, 8) #01
		datacontent += self.pack(state02, 8) #02
		datacontent += self.pack(state03, 8) #03
		datacontent += self.pack(state04, 8) #04
		datacontent += self.pack(state05, 8) #05
		datacontent += self.pack(state06, 8) #06
		datacontent += self.pack(state07, 8) #07
		datacontent += self.pack(state08, 8) #08
		datacontent += self.pack(state09, 8) #09
		return datatype, datacontent
	
	def create022d(self):
		"""HEARTスキル""" #before login and after map load
		datatype = "022d"
		datacontent = "03" #スキルの数
		datacontent += "2774" #スキルID
		datacontent += "2775" #スキルID
		datacontent += "2776" #スキルID
		return datatype, datacontent
		
	def create0223(self):
		"""属性値""" #before login
		datatype = "0223" #属性値
		datacontent = "07" #num
		datacontent += "0000" #新生属性？攻撃
		datacontent += "0000" #火
		datacontent += "0000" #水
		datacontent += "0000" #風
		datacontent += "0000" #土
		datacontent += "0000" #光
		datacontent += "0000" #闇
		datacontent += "07" #num
		datacontent += "0000" #新生属性？防御
		datacontent += "0000" #火
		datacontent += "0000" #水
		datacontent += "0000" #風
		datacontent += "0000" #土
		datacontent += "0000" #光
		datacontent += "0000" #闇
		return datatype, datacontent
		
	def create1bbc(self):
		"""スタンプ帳詳細""" #before login
		datatype = "1bbc" #スタンプ帳の詳細を表示
		datacontent = "0b" #ジャンル数 常に0b
		datacontent += "0000" #スペシャル
		datacontent += "0000" #プルル
		datacontent += "0000" #平原
		datacontent += "0000" #海岸
		datacontent += "0000" #荒野
		datacontent += "0000" #大陸ダンジョン
		datacontent += "0000" #雪国
		datacontent += "0000" #廃炭鉱ダンジョン
		datacontent += "0000" #ノーザンダンジョン
		datacontent += "0000" #アイアンサウス
		datacontent += "0000" #サウスダンジョン
		return datatype, datacontent
	
	def create025d(self):
		"""不明""" #before login
		datatype = "025d" #不明
		datacontent = "00" #不明
		return datatype, datacontent
	
	def create0695(self):
		"""不明""" #before login
		datatype = "0695" #不明
		datacontent = "00000002" #不明
		datacontent += "00" #不明
		return datatype, datacontent
	
	def create0236(self):
		"""wrp ranking関係""" #before login
		datatype = "0236" #自キャラのWRP順位と何か
		datacontent = "00000000" #不明
		datacontent += "00000000" #wrpの順位
		return datatype, datacontent

	def create1389(self, pc, skillid, targetsid, x, y, skilllv, error=0, cast=0):
		"""スキル使用通知"""
		datatype = "1389" #スキルを使用した際にサーバーから通知
		datacontent = self.pack(skillid, 4) #スキルID
		datacontent += self.pack(error, 2) #エラー値 [00]成功時。失敗時に値が入っている。
		datacontent += self.pack(pc.sid, 8) #スキル使用者のサーバキャラID
		datacontent += self.pack(cast, 8) #詠唱時間っぽ（ミリ秒単位）。失敗時は-1
		datacontent += self.pack(targetsid, 8) #スキル対象者のサーバキャラID。失敗時は-1
		datacontent += self.pack(x, 2) #x
		datacontent += self.pack(y, 2) #y
		datacontent += self.pack(skilllv, 2) #スキルLv
		datacontent += "00" #H.E.ARTを使ったときの白い玉の数
		return datatype, datacontent

	def create138a(self, pc, error):
		"""スキル使用通知"""
		datatype = "1389" #スキル使用通知
		datacontent = self.pack(pc.sid, 8) #サーバキャラID
		datacontent += self.pack(error, 2) #エラー値？
		return datatype, datacontent

	def create1392(self, pc, targetlist, skillid, skilllv, damagelist=None):
		"""スキル使用結果通知（対象：単体）"""
		targetlist_length = len(targetlist)
		if not damagelist:
			damagelist = []
			for i in xrange(targetlist_length):
				damagelist.append(0)
			no_damage_color_flag = True
		else:
			no_damage_color_flag = False
		damagelist_length = len(damagelist)
		datatype = "1392" #スキル成功時に対象へスキル効果を送られる
		datacontent = self.pack(skillid, 4) #スキルID
		
		datacontent += self.pack(targetlist_length, 2) #不明の数
		for x in xrange(targetlist_length):
			datacontent += "00" #不明
		
		datacontent += self.pack(pc.sid, 8) #使用キャラのサーバキャラID
		
		if targetlist:
			datacontent += self.pack(targetlist[0], 8) #対象のサーバキャラID #エフェクトが出る対象？
		else:
			datacontent += "00000000"
		datacontent += self.pack(targetlist_length, 2) #対象キャラ数
		for target in targetlist:
			datacontent += self.pack(target, 8) #対象キャラのサーバキャラID
		
		datacontent += self.pack(pc.x, 2) #x #不明
		datacontent += self.pack(pc.y, 2) #y #不明
		
		datacontent += self.pack(damagelist_length, 2) #HPダメージ数
		for damage in damagelist:
			datacontent += self.pack(damage, 8) #HPダメージ
		
		datacontent += self.pack(damagelist_length, 2) #MPダメージ数
		for x in xrange(damagelist_length):
			datacontent += "00000000" #MPダメージ
		
		datacontent += self.pack(damagelist_length, 2) #SPダメージ数
		for x in xrange(damagelist_length):
			datacontent += "00000000" #SPダメージ
		
		datacontent += self.pack(damagelist_length, 2) #数字の色の数
		for x in xrange(damagelist_length):
			if no_damage_color_flag:
				datacontent += "00000000" #なし
			elif int(damage) >= 0:
				datacontent += "00000001" #数字の色 #HPダメージ
			else:
				datacontent += "00000011" #数字の色 #HP回復
		datacontent += self.pack(skilllv, 2)
		return datatype, datacontent