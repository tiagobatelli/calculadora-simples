import pytest
from engine import CalculadoraEngine

engine = CalculadoraEngine()

def test_soma():
    assert engine.calcular_expressao("2+2") == "4"

def test_subtracao():
    assert engine.calcular_expressao("10-3") == "7"

def test_multiplicacao():
    assert engine.calcular_expressao("3*4") == "12"

def test_divisao():
    assert engine.calcular_expressao("10/2") == "5"

def test_divisao_por_zero():
    assert engine.calcular_expressao("5/0") == "Erro"

def test_expressao_com_parenteses():
    assert engine.calcular_expressao("(2+3)*4") == "20"

def test_porcentagem():
    assert engine.porcentagem("50") == "0.5"

def test_memoria():
    engine.ultimo_resultado = 42.0
    engine.memoria_mais()
    assert engine.memoria_recall() == "42"

def test_memoria_clear():
    engine.memoria_clear()
    assert engine.memoria == 0