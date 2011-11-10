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
	
#from consts import const
#print const.xxx.yyy
	
def setattr_for_const(self, name, value):
	if self.__dict__.get("init"):
		print "[const]", "setattr error / this class are not writeable /", name, value
		return
	else:
		self.__dict__[name] = value
	
class init:
	#writeable before exit
	def __init__(self, const_class):
		self.const_class = const_class
	
	def __enter__(self, *args):
		self.const_class.__dict__["init"] = False
	
	def __exit__(self, *args):
		self.const_class.__dict__["init"] = True
	
class Const:
	def __setattr__(self, name, value):
		setattr_for_const(self, name, value)
	
	def __init__(self):
		with init(self):
			attrs = tuple(dir(self))
			for a in attrs:
				if len(a) < 5:
					continue
				if not a.startswith("__"):
					continue
				if not a.endswith("__"):
					continue
				s = a.replace("__","")
				if not s[0].isupper():
					continue
				#self.__Job__.__setattr__ = setattr_for_const # etc...
				eval("self."+a).__setattr__ = setattr_for_const
				#self.job = self.__Job__() # etc ...
				self.__setattr__(s.lower(), eval("self."+a)())
				#self.job.init = True
				eval("self."+s.lower()).__dict__["init"] = True
	
	class __Job__: #private class #"_Const__Job__"
		"""編集"""
		def __init__(self):
			self.Novice = 0x00 	#ノービス
			self.Joker = 0x78		#ジョーカー
			self.SwordMan = 0x01		#ソードマン
			self.BladeMaster = 0x03		#ブレイドマスター
			self.Bountyhunter = 0x05	#バウンティハンター
			self.Gladiator = 0x07		#グラディエイター
			self.Fencer = 0x0B		#フェンサー
			self.Knight = 0x0D		#ナイト
			self.Darkstalker = 0x0F	#ダークストーカー
			self.Guardian = 0x11	#ガーディアン
			self.Scout = 0x15			#スカウト
			self.Assassin = 0x17		#アサシン
			self.Commando = 0x19		#コマンド
			self.Eraser = 0x21			#イレイザー
			self.Archer = 0x1F		#アーチャー
			self.Striker = 0x21	#ストライカー
			self.Gunner = 0x23		#ガンナー
			self.Hawkeye = 0x25	#ホークアイ
			self.Wizard = 0x29			#ウィザード
			self.Sorcerer = 0x2B		#ソーサラー
			self.Sage = 0x2D			#セージ
			self.ForceMaster = 0x2F		#フォースマスター
			self.Shaman = 0x33		#シャーマン
			self.Elementaler = 0x35	#エレメンタラー
			self.Enchanter = 0x37	#エンチャンター
			self.Astralist = 0x39	#アストラリスト
			self.Wotes = 0x3D			#ウァテス
			self.Druid = 0x3F			#ドルイド
			self.Bard = 0x41			#バード
			self.Cardinal = 0x43		#カーディナル
			self.Warlock = 0x47	#ウォーロック
			self.Cabalist = 0x49	#カバリスト
			self.Necromancer = 0x4B	#ネクロマンサー
			self.SoulTaker = 0x4D	#ソウルテイカー
			self.Tatarabe = 0x51		#タタラベ
			self.Blacksmith = 0x53		#ブラックスミス
			self.Machinery = 0x55		#マシンナリー
			self.Maestro = 0x57		#マエストロ
			self.Farmer = 0x5B		#ファーマー
			self.Alchemist = 0x5D	#アルケミスト
			self.Marionest = 0x5F	#マリオネスト
			self.Harvest = 0x61	#ハーヴェスト
			self.Ranger = 0x65			#レンジャー
			self.Explorer = 0x67		#エクスプローラー
			self.Treasureunter = 0x69	#トレジャーハンター
			self.Stryder = 0x6B		#ストライダー
			self.Merchant = 0x6F	#マーチャント
			self.Trader = 0x71		#トレーダー
			self.Gambler = 0x73	#ギャンブラー
			self.RoyalDealer = 0x75	#ロイヤルディーラー
			self.Breeder = 0xFF		#ブリーダー	#unknow
			self.Gardener = 0xFF		#ガーデナー	#unknow
			self.DEM = 0xFF		#DEM			#...
	
	class __HairColor__:
		"""ヘアカラー"""
		def __init__(self):
			self.Unknow = 0		#不明
			self.Red = 1			#レッド
			self.ShadePurple = 2	#ジェードパープル
			self.Blue = 3			#ブルー
			self.IceBlue = 4		#アイスブルー
			self.Green = 5		#グリーン
			self.LightGreen = 6	#ライトグリーン
			self.CandyYellow = 7	#キャンディーイエロー
			self.Orange = 8		#オレンジ
			self.MatteBlack = 9	#マットブラック
			self.DullGrey = 10		#ダルグレー
			self.Silver = 11		#シルバー
			self.MoistSilver = 12	#モイストシルバー
			self.HoneyBeige = 50		#ハニーベージュ
			self.CocoaBrown = 51		#ココアブラウン
			self.BitterBrown = 52		#ビターブラウン
			self.WhiteGold = 60	#ホワイトゴールド
			self.PlatinaBlond = 61	#プラチナブロンド
			self.ChampagneGold = 62	#シャンパンゴールド
			self.Rose = 70			#ローズ
			self.WineRed = 71			#ワインレッド
			self.DarkCherry = 72		#ダークチェリー
	
	class __Part__:
		"""アイテムの保管場所"""
		def __init__(self):
			self.IBody = 2		#体 (インベントリ)
			self.IRight = 3		#右手 (インベントリ)
			self.ILeft = 4		#左手 (インベントリ)
			self.IBack = 5		#背中 (インベントリ)
			self.OtherWarehouse = 0		#別の倉庫
			self.Warehouse	 = 30		#倉庫
			self.GardenWarehouse = 51	#飛空庭倉庫
			self.Head = 6			#頭
			self.HeadA = 7		#頭アクセサリー
			self.FaceA = 8		#顔アクセサリー
			self.Face = 9			#顔
			self.ChestA = 10		#胸アクセサリー
			self.Tops = 11		#上半身
			self.Buttoms = 12		#下半身
			self.Back = 13		#背中
			self.Right = 14		#右手
			self.Left = 15		#左手
			self.Shoes = 16		#靴
			self.Socks = 17		#靴下
			self.Pet = 18			#ペット
			self.InventoryBody = self.IBody	#体 (インベントリ)
			self.InventoryRight = self.IRight	#右手 (インベントリ)
			self.InventoryLeft = self.ILeft	#左手 (インベントリ)
			self.InventoryBack = self.IBack	#背中 (インベントリ)
			self.HeadAccessory = self.HeadA	#頭アクセサリー
			self.FaceAccessory = self.FaceA	#顔アクセサリー
			self.ChestAccessory = self.ChestA	#胸アクセサリー
			self.Accessory = self.ChestA		#胸アクセサリー
	
	#end
	
const = Const()
	
if __name__ == "__main__":
	print "--- const test ---"
	print "const.part.InventoryBack", const.part.InventoryBack
	const.part.InventoryBack = 1
	print "const.part.InventoryBack", const.part.InventoryBack
	
	