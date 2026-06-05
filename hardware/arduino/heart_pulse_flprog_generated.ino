#include "flprogUtilites.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <EEPROM.h>
LiquidCrystal_I2C _lcd1(0x27, 16, 2);
int _dispTempLength1=0;
boolean _isNeedClearDisp1;
const int _menuParametrsArray[]  PROGMEM =  {1, 4, 1, 0, 0, 0, 2, 3, 1, 4, 1, 0, 2, 4, 2, 0, 0, 0, 2, 3, 1, 4, 3, 0, 3, 3, 1, 0, 0, 0, 4, 5, 1, 8, 2, 0};
bool _menuValueArray_bool[1];
const bool _menuConstantValuesArray_bool[]  PROGMEM =  {1, 0};
int _menuValueArray_int[2];
const int _menuConstantValuesArray_int[]  PROGMEM =  {1, 1000, 0};
const char _flprogMenuNameString1[] PROGMEM = "Instal ml";
const char _flprogMenuNameString2[] PROGMEM = "Neprerivno";
const char _flprogMenuNameString3[] PROGMEM = "Instal liter";
const char _flprogMenuNameString4[] PROGMEM = "On";
const char _flprogMenuNameString5[] PROGMEM = "Off";
const char* const _flprogMenuStringsArray[] PROGMEM = { _flprogMenuNameString1,  _flprogMenuNameString2,  _flprogMenuNameString3,  _flprogMenuNameString4,  _flprogMenuNameString5};
struct _menuItemStricture 
{
     int startInArrayIndex;
}
;
struct _menuMainStricture 
{
    int startIndex;
    int stopIndex;
    bool isSwitchMenuAroundRing;
    _menuItemStricture  currentItem;
}
;
_menuItemStricture _MenuItems[3];
_menuMainStricture _MainMenus[1];
unsigned long _gtv3;
bool _gtv4 = 0;
float _gtv5;
float _gtv6;
bool _MenuBlock_154348375_AMO_58956816 = 0;
bool _MenuBlock_154348375_AMO_6175933 = 0;
bool _MenuBlock_154348375_AMO_126755350 = 0;
String _MenuBlock_154348375_MNO;
String _MenuBlock_154348375_VNO;
bool _MenuBlock_154348375_OEIS = 0;
bool _MenuBlock_154348375_OMUIS = 0;
bool _MenuBlock_154348375_OMDIS = 0;
bool _MenuBlock_154348375_OVUIS = 0;
bool _MenuBlock_154348375_OVDIS = 0;
unsigned long _MenuBlock_154348375_VUDST = 0UL;
unsigned long _MenuBlock_154348375_VUDSPT = 0UL;
int _MenuBlock_154348375_VUDSM = 0;
int _MenuBlock_154348375_VUDPT = 0;
String _swi1;
String _swi2;
bool _bounseInputD4S = 0;
bool _bounseInputD4O = 0;
unsigned long _bounseInputD4P = 0UL;
bool _trgrt2 = 0;
bool _trgrt2I = 0;
bool _trgs1 = 0;
bool _bounseInputD5S = 0;
bool _bounseInputD5O = 0;
unsigned long _bounseInputD5P = 0UL;
bool _tim3I = 0;
bool _tim3O = 0;
unsigned long _tim3P = 0UL;
bool _trgrt1 = 0;
bool _trgrt1I = 0;
bool _bounseInputD6S = 0;
bool _bounseInputD6O = 0;
unsigned long _bounseInputD6P = 0UL;
bool _tim2I = 0;
bool _tim2O = 0;
unsigned long _tim2P = 0UL;
int _disp4oldLength = 0;
bool _bounseInputD7S = 0;
bool _bounseInputD7O = 0;
unsigned long _bounseInputD7P = 0UL;
bool _count2I = 0;
int _count2_Value = 0;
int _disp1oldLength = 0;
bool _trgrt3 = 0;
bool _trgrt3I = 0;
bool _count1I = 0;
int _count1_Value = 0;
int _disp5oldLength = 0;
int _disp3oldLength = 0;
int _disp2oldLength = 0;
bool _trgs2 = 0;
bool _tempVariable_bool;
int _tempVariable_int;
void setup()
{
    pinMode(4, INPUT_PULLUP);
    pinMode(5, INPUT_PULLUP);
    pinMode(6, INPUT_PULLUP);
    pinMode(7, INPUT_PULLUP);
    pinMode(2, INPUT);
    pinMode(9, OUTPUT);
    digitalWrite(9, 0);
    pinMode(13, OUTPUT);
    digitalWrite(13, 0);
    Wire.begin();
    delay(10);
    if(((readByteFromEEPROM(0, 0, 0x0))) != 117) 
    {
        (updateByteToEEPROM(0, 0, 0x0, (117)));
        (updateBooleanToEEPROM(1, 0, 0x0, (0)));
        (updateIntegerToEEPROM(2, 0, 0x0, (50)));
        (updateIntegerToEEPROM(4, 0, 0x0, (0)));
    }
    _lcd1.init();
    _lcd1.backlight();
    _bounseInputD6O =    digitalRead(6);
    _bounseInputD5O =    digitalRead(5);
    _bounseInputD7O =    digitalRead(7);
    _bounseInputD4O =    digitalRead(4);
    _MenuItems[0].startInArrayIndex = 0;
    _MenuItems[1].startInArrayIndex = 12;
    _MenuItems[2].startInArrayIndex = 24;
    _MainMenus[0].startIndex = 1;
    _MainMenus[0].isSwitchMenuAroundRing = 1;
    _MainMenus[0].stopIndex = 3;
    _MainMenus[0].currentItem = _MenuItems[0];
    _menuValueArray_int[0] = (readIntegerFromEEPROM(2, 0, 0x0));
    _menuValueArray_bool[0] = (readBooleanFromEEPROM(1, 0, 0x0));
    _menuValueArray_int[1] = (readIntegerFromEEPROM(4, 0, 0x0));
}
void loop()
{
    if (_isNeedClearDisp1) 
    {
        _lcd1.clear();
        _isNeedClearDisp1= 0;
    }
    bool  _bounceInputTmpD6 =  (digitalRead (6));
    if (_bounseInputD6S)
    {
        if (millis() >= (_bounseInputD6P + 40))
        {
            _bounseInputD6O= _bounceInputTmpD6;
            _bounseInputD6S=0;
        }
    }
    else
    {
        if (_bounceInputTmpD6 != _bounseInputD6O)
        {
            _bounseInputD6S=1;
            _bounseInputD6P = millis();
        }
    }
    bool  _bounceInputTmpD4 =  (digitalRead (4));
    if (_bounseInputD4S)
    {
        if (millis() >= (_bounseInputD4P + 40))
        {
            _bounseInputD4O= _bounceInputTmpD4;
            _bounseInputD4S=0;
        }
    }
    else
    {
        if (_bounceInputTmpD4 != _bounseInputD4O)
        {
            _bounseInputD4S=1;
            _bounseInputD4P = millis();
        }
    }
    bool  _bounceInputTmpD5 =  (digitalRead (5));
    if (_bounseInputD5S)
    {
        if (millis() >= (_bounseInputD5P + 40))
        {
            _bounseInputD5O= _bounceInputTmpD5;
            _bounseInputD5S=0;
        }
    }
    else
    {
        if (_bounceInputTmpD5 != _bounseInputD5O)
        {
            _bounseInputD5S=1;
            _bounseInputD5P = millis();
        }
    }
    bool  _bounceInputTmpD7 =  (digitalRead (7));
    if (_bounseInputD7S)
    {
        if (millis() >= (_bounseInputD7P + 40))
        {
            _bounseInputD7O= _bounceInputTmpD7;
            _bounseInputD7S=0;
        }
    }
    else
    {
        if (_bounceInputTmpD7 != _bounseInputD7O)
        {
            _bounseInputD7S=1;
            _bounseInputD7P = millis();
        }
    }
    //Плата:1
//Наименование:Счетчик
    if (!(_bounseInputD7O)) 
    {
         if (_trgrt1I) 
        {
             _trgrt1 = 0;
        }
         else 
        {
            _trgrt1 = 1;
            _trgrt1I = 1;
        }
    }
     else 
    {
        _trgrt1 = 0;
        _trgrt1I = 0;
    }
    ;
    if ((digitalRead (2))) 
    {
         if (_trgrt3I) 
        {
             _trgrt3 = 0;
        }
         else 
        {
            _trgrt3 = 1;
            _trgrt3I = 1;
        }
    }
     else 
    {
        _trgrt3 = 0;
        _trgrt3I = 0;
    }
    ;
    if (_trgrt1)
    {
        _count2_Value = 0;
    }
     else 
    {
        if (_trgrt3)
        {
            if (! _count2I) 
            {
                _count2I = 1;
                _count2_Value = _count2_Value + 1;
            }
        }
         else 
        {
            _count2I = 0;
        }
    }
    _gtv3 = _count2_Value;
    //Плата:2
//Наименование:Блок меню
    if (!(((!(_bounseInputD4O)) || (!(_bounseInputD5O)) || (!(_bounseInputD6O)))))
    {
         if (_tim2I) 
        {
             if (flprog::isTimer(_tim2P, 5000)) 
            {
                _tim2O = 1;
            }
        }
         else 
        {
            _tim2I =1;
            _tim2P = millis();
        }
    }
     else 
    {
        _tim2O = 0;
        _tim2I = 0;
    }
    if(!(_bounseInputD4O)) _trgs1 = 1;
    if(_tim2O) _trgs1 = 0;
    _gtv4 = _trgs1;
    if (_gtv4) 
    {
        _tempVariable_bool  =  1;
        if (! _MenuBlock_154348375_OEIS) 
        {
            _MenuBlock_154348375_OEIS = 1;
        }
        _tempVariable_int = pgm_read_byte(&_menuParametrsArray[((_MainMenus[0].currentItem).startInArrayIndex)+10]);
        _MenuBlock_154348375_MNO = _readStringFromProgmem ((char*)pgm_read_word(&(_flprogMenuStringsArray[_tempVariable_int - 1])));
        _MenuBlock_154348375_VNO = _menuOutputValueString (0);
        _MenuBlock_154348375_AMO_58956816 = pgm_read_byte(&_menuParametrsArray[(_MainMenus[0].currentItem).startInArrayIndex]) == 1;
        _MenuBlock_154348375_AMO_6175933 = pgm_read_byte(&_menuParametrsArray[(_MainMenus[0].currentItem).startInArrayIndex]) == 2;
        _MenuBlock_154348375_AMO_126755350 = pgm_read_byte(&_menuParametrsArray[(_MainMenus[0].currentItem).startInArrayIndex]) == 3;
    }
     else 
    {
        _tempVariable_bool  =  0;
        if (_MenuBlock_154348375_OEIS)
        {
            _MenuBlock_154348375_OEIS = 0;
            _menuUpdateToEEpromItems();
        }
        _MenuBlock_154348375_AMO_58956816 = 0;
        _MenuBlock_154348375_AMO_6175933 = 0;
        _MenuBlock_154348375_AMO_126755350 = 0;
        _MenuBlock_154348375_MNO = "";
        _MenuBlock_154348375_VNO = "";
    }
    if(0) 
    {
         if (! _MenuBlock_154348375_OMUIS) 
        {
            _MenuBlock_154348375_OMUIS = 1;
            if(_tempVariable_bool)
            {
                _menuUpEvents(0);
                _menuUpdateToEEpromItems();
            }
        }
    }
     else 
    {
        _MenuBlock_154348375_OMUIS = 0;
    }
    if(!(_bounseInputD4O)) 
    {
         if (! _MenuBlock_154348375_OMDIS) 
        {
            _MenuBlock_154348375_OMDIS = 1;
            if(_tempVariable_bool)
            {
                _menuDownEvents(0);
                _menuUpdateToEEpromItems();
            }
        }
    }
     else 
    {
        _MenuBlock_154348375_OMDIS = 0;
    }
    if(!(_bounseInputD5O)) 
    {
         if (! _MenuBlock_154348375_OVUIS) 
        {
            _MenuBlock_154348375_OVUIS = 1;
            if(_tempVariable_bool)
            {
                  _valueUpEvents(0);
                _MenuBlock_154348375_VUDST = millis();
            }
        }
        if (_tempVariable_bool)
        {
            if (_MenuBlock_154348375_VUDSM == 0) 
            {
                 if (flprog::isTimer(_MenuBlock_154348375_VUDST , 2000)) 
                {
                    _MenuBlock_154348375_VUDSM = 1;
                    _MenuBlock_154348375_VUDSPT = millis();
                    _MenuBlock_154348375_VUDPT  = 500;
                }
            }
              else 
            {
                 if (_MenuBlock_154348375_VUDSM == 1) 
                {
                     if (flprog::isTimer(_MenuBlock_154348375_VUDST , 4000)) 
                    {
                        _MenuBlock_154348375_VUDSM = 2;
                        _MenuBlock_154348375_VUDPT  = 250;
                    }
                }
                 if (flprog::isTimer(_MenuBlock_154348375_VUDSPT , _MenuBlock_154348375_VUDPT)) 
                {
                     _valueUpEvents(0);
                    _MenuBlock_154348375_VUDSPT = millis();
                }
            }
        }
    }
     else 
    {
        _MenuBlock_154348375_OVUIS = 0;
        if(! (!(_bounseInputD6O)))
        {
            _MenuBlock_154348375_VUDSM = 0;
        }
    }
    if(!(_bounseInputD6O)) 
    {
         if (! _MenuBlock_154348375_OVDIS) 
        {
            _MenuBlock_154348375_OVDIS = 1;
            if(_tempVariable_bool)
            {
                  _valueDownEvents(0);
                _MenuBlock_154348375_VUDST = millis();
            }
        }
         if (_tempVariable_bool)
        {
            if (_MenuBlock_154348375_VUDSM == 0) 
            {
                 if (flprog::isTimer(_MenuBlock_154348375_VUDST , 2000)) 
                {
                    _MenuBlock_154348375_VUDSM = 1;
                    _MenuBlock_154348375_VUDSPT = millis();
                    _MenuBlock_154348375_VUDPT  = 500;
                }
            }
              else 
            {
                 if (_MenuBlock_154348375_VUDSM == 1) 
                {
                     if (flprog::isTimer(_MenuBlock_154348375_VUDST , 4000)) 
                    {
                        _MenuBlock_154348375_VUDSM = 2;
                        _MenuBlock_154348375_VUDPT  = 250;
                    }
                }
                 if (flprog::isTimer(_MenuBlock_154348375_VUDSPT , _MenuBlock_154348375_VUDPT)) 
                {
                     _valueDownEvents(0);
                    _MenuBlock_154348375_VUDSPT = millis();
                }
            }
        }
    }
     else 
    {
        _MenuBlock_154348375_OVDIS = 0;
        if(! (!(_bounseInputD5O)))
        {
            _MenuBlock_154348375_VUDSM = 0;
        }
    }
    if(_MenuBlock_154348375_AMO_58956816)
    {
        _swi1=((_MenuBlock_154348375_VNO) + (String(" ml")));
    }
    else
    {
        _swi1=((_MenuBlock_154348375_VNO) + (String(" Liter")));
    }
    if(_MenuBlock_154348375_AMO_126755350)
    {
        _swi2=_MenuBlock_154348375_VNO;
    }
    else
    {
        _swi2=_swi1;
    }
    if (_gtv4) 
    {
        _dispTempLength1 = ((_swi2)).length();
        if (_disp2oldLength > _dispTempLength1) 
        {
            _isNeedClearDisp1 = 1;
        }
        _disp2oldLength = _dispTempLength1;
        _lcd1.setCursor(int((16 - _dispTempLength1)/2), 1);
        _lcd1.print((_swi2));
    }
     else 
    {
        if (_disp2oldLength > 0) 
        {
            _isNeedClearDisp1 = 1;
            _disp2oldLength = 0;
        }
    }
    if (_gtv4) 
    {
        _dispTempLength1 = ((_MenuBlock_154348375_MNO)).length();
        if (_disp1oldLength > _dispTempLength1) 
        {
            _isNeedClearDisp1 = 1;
        }
        _disp1oldLength = _dispTempLength1;
        _lcd1.setCursor(int((16 - _dispTempLength1)/2), 0);
        _lcd1.print((_MenuBlock_154348375_MNO));
    }
     else 
    {
        if (_disp1oldLength > 0) 
        {
            _isNeedClearDisp1 = 1;
            _disp1oldLength = 0;
        }
    }
    //Плата:3
    _gtv6 = (_gtv3)/(2800.00);
    if (!(_gtv4)) 
    {
        _dispTempLength1 = (((((_floatToStringWitRaz((_gtv3)/(2800.00),2))) + (String(" L"))))).length();
        if (_disp3oldLength > _dispTempLength1) 
        {
            _isNeedClearDisp1 = 1;
        }
        _disp3oldLength = _dispTempLength1;
        _lcd1.setCursor(0, 0);
        _lcd1.print(((((_floatToStringWitRaz((_gtv3)/(2800.00),2))) + (String(" L")))));
    }
     else 
    {
        if (_disp3oldLength > 0) 
        {
            _isNeedClearDisp1 = 1;
            _disp3oldLength = 0;
        }
    }
    //Плата:4
//Наименование:Установлено литров
    _gtv5 = ((_menuValueArray_int[1]))+(((_menuValueArray_int[0]))/(1000.00));
    if (!(_gtv4)) 
    {
        _dispTempLength1 = (((((_floatToStringWitRaz(((_menuValueArray_int[1]))+(((_menuValueArray_int[0]))/(1000.00)),2))) + (String("L"))))).length();
        if (_disp5oldLength > _dispTempLength1) 
        {
            _isNeedClearDisp1 = 1;
        }
        _disp5oldLength = _dispTempLength1;
        _lcd1.setCursor(9, 0);
        _lcd1.print(((((_floatToStringWitRaz(((_menuValueArray_int[1]))+(((_menuValueArray_int[0]))/(1000.00)),2))) + (String("L")))));
    }
     else 
    {
        if (_disp5oldLength > 0) 
        {
            _isNeedClearDisp1 = 1;
            _disp5oldLength = 0;
        }
    }
    //Плата:5
//Наименование:Счетчик циклов
    if (!(_bounseInputD7O)) 
    {
         if (_trgrt2I) 
        {
             _trgrt2 = 0;
        }
         else 
        {
            _trgrt2 = 1;
            _trgrt2I = 1;
        }
    }
     else 
    {
        _trgrt2 = 0;
        _trgrt2I = 0;
    }
    ;
    if (!(_bounseInputD5O))
    {
         if (_tim3I) 
        {
             if (flprog::isTimer(_tim3P, 3000)) 
            {
                _tim3O = 1;
            }
        }
         else 
        {
            _tim3I =1;
            _tim3P = millis();
        }
    }
     else 
    {
        _tim3O = 0;
        _tim3I = 0;
    }
    if (_tim3O)
    {
        _count1_Value = 0;
    }
     else 
    {
        if (_trgrt2)
        {
            if (! _count1I) 
            {
                _count1I = 1;
                _count1_Value = _count1_Value + 1;
            }
        }
         else 
        {
            _count1I = 0;
        }
    }
    if (!(_gtv4)) 
    {
        _dispTempLength1 = ((((String("Cikl ")) + ((String(_count1_Value, DEC)))))).length();
        if (_disp4oldLength > _dispTempLength1) 
        {
            _isNeedClearDisp1 = 1;
        }
        _disp4oldLength = _dispTempLength1;
        _lcd1.setCursor(0, 1);
        _lcd1.print((((String("Cikl ")) + ((String(_count1_Value, DEC))))));
    }
     else 
    {
        if (_disp4oldLength > 0) 
        {
            _isNeedClearDisp1 = 1;
            _disp4oldLength = 0;
        }
    }
    //Плата:6
//Наименование:Автомотика
    if(!(_bounseInputD7O)) _trgs2 = 1;
    if((((((_gtv6) >= (_gtv5)) && (!((_menuValueArray_bool[0]))))) || (!(_bounseInputD6O)))) _trgs2 = 0;
    digitalWrite(13, _trgs2);
    digitalWrite(9, !(_trgs2));
}
String  _floatToStringWitRaz(float value, int raz)
{
    return String(value,raz);
}
String _readStringFromProgmem (char *string)
{
    String result = String("");
    while (pgm_read_byte(string)!='\0')
    {
        result=result+ char(pgm_read_byte(string));
        	string++;
        	
    }
    return result;
}
void _menuUpEvents (int menuIndex)
{
    int tempIndex = pgm_read_byte(&_menuParametrsArray[((_MainMenus[menuIndex]).currentItem).startInArrayIndex]);
    int parIndex = pgm_read_byte(&_menuParametrsArray[ (((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+5]);
    int parentStartIndex;
    int parentStopIndex;
    if (parIndex == 0) 
    {
        parentStartIndex = (_MainMenus[menuIndex]).startIndex;
        parentStopIndex =(_MainMenus[menuIndex]).stopIndex;
    }
    else 
    {
        parentStartIndex = pgm_read_byte(&_menuParametrsArray[((_MenuItems[parIndex - 1]).startInArrayIndex)+3]);
        parentStopIndex = pgm_read_byte(&_menuParametrsArray[((_MenuItems[parIndex-1]).startInArrayIndex)+4]);
    }
    if (tempIndex == parentStartIndex) 
    {
        if((_MainMenus[menuIndex]).isSwitchMenuAroundRing) 
        {
            (_MainMenus[menuIndex]).currentItem = _MenuItems[parentStopIndex -1];
            return;
        }
         else
        {
            return;
        }
    }
    (_MainMenus[menuIndex]).currentItem = _MenuItems[tempIndex - 2];
    return;
}
void _menuDownEvents (int menuIndex)
{
    int tempIndex = pgm_read_byte(&_menuParametrsArray[((_MainMenus[menuIndex]).currentItem).startInArrayIndex]);
    int parIndex = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+5]);
    int parentStartIndex;
    int parentStopIndex;
    if (parIndex == 0) 
    {
        parentStartIndex = (_MainMenus[menuIndex]).startIndex;
        parentStopIndex =(_MainMenus[menuIndex]).stopIndex;
    }
    else 
    {
        parentStartIndex = pgm_read_byte(&_menuParametrsArray[((_MenuItems[parIndex-1]).startInArrayIndex)+3]);
        parentStopIndex = pgm_read_byte(&_menuParametrsArray[((_MenuItems[parIndex-1]).startInArrayIndex)+4]);
    }
    if (tempIndex == parentStopIndex) 
    {
        if((_MainMenus[menuIndex]).isSwitchMenuAroundRing) 
        {
            (_MainMenus[menuIndex]).currentItem = _MenuItems[parentStartIndex -1];
            return;
        }
         else
        {
            return;
        }
    }
    (_MainMenus[menuIndex]).currentItem = _MenuItems[tempIndex];
    return;
}
void _valueUpEvents (int menuIndex)
{
    int valIndex = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+2]);
    int itemType = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+1]);
    int indexMax = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+6]);
    int indexStep = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+8]);
    if(itemType ==3) 
    {
        _menuValueArray_bool[valIndex - 1 ] = 1;
        return;
    }
    if (itemType == 4) 
    {
        if (! indexMax == 0) 
        {
             if (! (int(pgm_read_word(&_menuConstantValuesArray_int[indexMax -1])) > int(_menuValueArray_int[valIndex -1]))) 
            {
                return;
            }
        }
        _menuValueArray_int[valIndex -1] = _menuValueArray_int[valIndex -1] + (pgm_read_word(&_menuConstantValuesArray_int[indexStep -1]));
    }
}
void _valueDownEvents (int menuIndex)
{
    int valIndex = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+2]);
    int itemType = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+1]);
    int indexMin = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+7]);
    int indexStep = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+8]);
    if(itemType ==3) 
    {
        _menuValueArray_bool[valIndex -1] = 0;
        return;
    }
    if (itemType == 4) 
    {
        if (! indexMin == 0) 
        {
             if (! ((int(pgm_read_word(&_menuConstantValuesArray_int[indexMin - 1]))) < int(_menuValueArray_int[valIndex - 1]))) 
            {
                return;
            }
        }
        _menuValueArray_int[valIndex - 1] = _menuValueArray_int[valIndex - 1] - (pgm_read_word(&_menuConstantValuesArray_int[indexStep - 1]));
    }
}
String _menuOutputValueString (int menuIndex)
{
    int itemType = pgm_read_byte(&_menuParametrsArray[ (((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+1]);
    int valIndex = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+2]);
    int indexMin = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+7]);
    int indexMax = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+6]);
    if(valIndex == 0)
    {
         return "";
    }
    int convFormat = pgm_read_byte(&_menuParametrsArray[(((_MainMenus[menuIndex]).currentItem).startInArrayIndex)+9]);
    if(itemType == 3) 
    {
         return _convertBoolean(itemType, convFormat, valIndex, indexMax, indexMin);
    }
    if(itemType == 4) 
    {
         return _convertNamber(itemType, convFormat, valIndex, indexMax, indexMin);
    }
    return "";
}
void _menuUpdateToEEpromItems()
{
    (updateIntegerToEEPROM(2, 0, 0x0, ((_menuValueArray_int[0]))));
    (updateBooleanToEEPROM(1, 0, 0x0, ((_menuValueArray_bool[0]))));
    (updateIntegerToEEPROM(4, 0, 0x0, ((_menuValueArray_int[1]))));
}
String _convertNamber(int itemType, int convFormat, int valIndex, int indexMax, int indexMin)
{
    if (itemType== 4) 
    {
        if (convFormat == 4) 
        {
             return String((_menuValueArray_int[valIndex - 1 ]),DEC);
        }
        if (convFormat == 5) 
        {
             return String((_menuValueArray_int[valIndex - 1]),HEX);
        }
        if (convFormat == 6) 
        {
             return String((_menuValueArray_int[valIndex -1]),BIN);
        }
    }
    return "";
}
String _convertBoolean(int itemType, int convFormat, int valIndex, int indexMax, int indexMin)
{
    if (convFormat == 1) 
    {
         if(_menuValueArray_bool[valIndex -1]) 
        {
            return "1";
        }
         else
        {
             return "0";
        }
    }
    if (convFormat == 2) 
    {
         if(_menuValueArray_bool[valIndex -1]) 
        {
            return "True";
        }
         else
        {
             return "False";
        }
    }
    if (convFormat == 3) 
    {
         if(_menuValueArray_bool[valIndex -1 ]) 
        {
            return "Да";
        }
         else
        {
             return "Нет";
        }
    }
    if(_menuValueArray_bool[valIndex -1]) 
    {
        return _readStringFromProgmem ((char*)pgm_read_word(&(_flprogMenuStringsArray[indexMax - 1])));
    }
     else 
    {
         return _readStringFromProgmem ((char*)pgm_read_word(&(_flprogMenuStringsArray[indexMin - 1])));
    }
    return "";
}
byte readByteFromEEPROM(int addres, byte bitAddres, byte chipAddres)
{
    return EEPROM.read(addres);
}
void updateByteToEEPROM(int addres, byte bitAddres, byte chipAddres, byte value)
{
    return EEPROM.update(addres, value);
}
bool readBooleanFromEEPROM(int addres, byte bitAddres, byte chipAddres)
{
    byte temp = readByteFromEEPROM(addres,  bitAddres,  chipAddres);
    return  bitRead(temp, bitAddres);
}
void updateBooleanToEEPROM(int addres, byte bitAddres, byte chipAddres, bool value)
{
    byte temp = readByteFromEEPROM(addres,  bitAddres,  chipAddres);
    bitWrite(temp, bitAddres, value);
    updateByteToEEPROM(addres,  bitAddres,  chipAddres, temp);
}
int readIntegerFromEEPROM(int addres, byte bitAddres, byte chipAddres)
{
    byte hight = readByteFromEEPROM(addres,  bitAddres,  chipAddres);
    byte low = readByteFromEEPROM((addres+1),  bitAddres,  chipAddres);
    return  word(hight, low);
}
void updateIntegerToEEPROM(int addres, byte bitAddres, byte chipAddres, int value)
{
    updateByteToEEPROM(addres,  bitAddres,  chipAddres, highByte(value));
    updateByteToEEPROM((addres+1),  bitAddres,  chipAddres, lowByte(value));
}