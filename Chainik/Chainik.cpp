// Chainik.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <vector>
#include <string>
#include <time.h>
#include <stdlib.h>
#include <cstdlib>
#include <iostream>
#include <windows.h>
#include<cstdlib>
#include<ctime>

#include <cstdarg>

using namespace std;


/*
class Target
{
public:
	int volume;
	int water;
	int water2 = 0;
	int timeboil;
	int timeforfill;
	
	
	virtual int timeforboiling(int water) = 0;
	virtual bool empty_or_not(int water, int water2) = 0;
	virtual void waterr(int water2) = 0;
	virtual void watermin() = 0;
};

class Target1 : public Target
{
public:
	int volume = 500; //допустимый обьем чайника
	int water = 0;//вода в чайнике
	int water2 = 0;//сколько хочет налить пользователь
	int timeboil = 10;//

	int timeforfill = 1;
	bool Isempty = false;
	
	
	void waterr(int water2) override
	{
		if ((water + water2) > volume) {
			water = volume;
			cout << "Кипятим максимальный обьем " << volume << endl;
		}
		else {
			water = water + water2;
		}
		
		
	}
	void watermin() override
	{
		water = 0;
	}
	int timeforboiling(int water2) override
	{
		//cout << chance << endl;//0.
		timeboil =  water2 / 100;
		return timeboil;
	}
	bool empty_or_not(int water,int water2) override
	{
		if (water==0)
		{
			//water = water2;
			return true;
		}
		else
		{
			return false;
		}
	}
};
class Kitchen
{
public:
	Target1 teapot;
	int proc(int ml){
		int timeproc = 0;
		if (teapot.empty_or_not(teapot.water, ml) == true)
		{
			teapot.waterr(ml);
			timeproc += teapot.timeforfill;
			timeproc += teapot.timeforboiling(teapot.water);
			cout << "Время было затрачено:  " << timeproc<<endl;
			return timeproc;
		}
		else {
			cout << "Чайник полный" << endl;
			teapot.watermin();
			timeproc += teapot.timeforfill;
			cout << "Вылили воду:  " << teapot.timeforfill<<"min" << endl;
			teapot.waterr(ml);
			timeproc += teapot.timeforfill;
			cout << "Налили воду:  " << teapot.timeforfill << "min" << endl;
			timeproc += teapot.timeforboiling(teapot.water);
			cout << "Кипятим воду:  " << teapot.timeforboiling(teapot.water) << "min" << endl;
			cout << "Время было затрачено:  " << timeproc << endl;
			return timeproc;
			
		}
	}
	


};


int main()
{
	setlocale(LC_ALL, "Russian");
	int k;
	bool var = true;
	int ml;
	cout << "Вы на кухне!" << "\nНажмите 1, чтобы вскипятить чайник." << "\nНажмите 2, чтобы выйти";
	Kitchen kit;
	do {
		cin >> k; // ввод значения
		switch (k)
		{
		case 1:
			cout << "Сколько мл воды вы хотите налить в чайник?";
			cin >> ml;
			kit.proc(ml);
			break;
		case 2:

			break;
		default:
			cout << "выберите значение из списка" << "\n";
			break;
		}
		if (k == 2)
			var = false;
	} while (var);
}
*/
 class Target
{
public:
	int volume;
	int water;
	int water2 = 0;
	int timeboil;
	int timeforfill;


	virtual int timeforboiling(int water) = 0;
	virtual bool empty_or_not(int water, int water2) = 0;
	virtual void waterr(int water2) = 0;
	virtual void watermin() = 0;
};

class Target1 : public Target
{
public:
	int volume = 500; //допустимый обьем чайника
	int water = 0;//вода в чайнике
	int water2 = 0;//сколько хочет налить пользователь
	int timeboil = 10;//
	int timeforfill = 1;
	bool Isempty = false;


	void waterr(int water2) override
	{
		if ((water + water2) > volume) {
			water = volume;
			cout << "Кипятим максимальный обьем " << volume << endl;
		}
		else {
			water = water + water2;
		}
	}
	void watermin() override
	{
		water = 0;
	}
	int timeforboiling(int water2) override
	{
		//cout << chance << endl;//0.
		timeboil = water2 / 100;
		return timeboil;
	}
	bool empty_or_not(int water, int water2) override
	{
		if (water == 0)
		{
			//water = water2;
			return true;
		}
		else
		{
			return false;
		}
	}
};
class Kitchen
{
public:
	Target1 teapot;
	int o = 0;
	int proc(int ml) {
		int timeproc = 0;
		if (teapot.empty_or_not(teapot.water, ml) == true)
		{
			teapot.waterr(ml);
			timeproc += teapot.timeforfill;
			timeproc += teapot.timeforboiling(teapot.water);
			cout << "Время было затрачено:  " << timeproc << endl;
			return timeproc;
		}
		else {
			cout << "В чайнике уже "<< teapot.water <<" ml"<<"1.Долить полный 2.Кипятить что есть"  << endl;
			cin >> o;
			
				switch (o)
				{
				case 1:
					teapot.waterr(ml);
					timeproc += teapot.timeforfill;
					timeproc += teapot.timeforboiling(teapot.volume);
					cout << "Время было затрачено:  " << timeproc << endl;
					return timeproc;
					break;
				case 2:
					timeproc += teapot.timeforboiling(teapot.water);
					cout << "Кипятим воду:  " << teapot.timeforboiling(teapot.water) << "min" << endl;
					cout << "Время было затрачено:  " << timeproc << endl;
					return timeproc;
					break;
				default:
					cout << "выберите значение из списка" << "\n";
					break;
				}

			

		}
	}
};


int main()
{
	setlocale(LC_ALL, "Russian");
	int k;
	bool var = true;
	int ml;
	cout << "Вы на кухне!" << "\nНажмите 1, чтобы вскипятить чайник." << "\nНажмите 2, чтобы выйти";
	Kitchen kit;
	do {
		cin >> k; // ввод значения
		switch (k)
		{
		case 1:
			cout << "Сколько мл воды вы хотите налить в чайник?";
			cin >> ml;
			kit.proc(ml);
			break;
		case 2:

			break;
		default:
			cout << "выберите значение из списка" << "\n";
			break;
		}
		if (k == 2)
			var = false;
	} while (var);
}
