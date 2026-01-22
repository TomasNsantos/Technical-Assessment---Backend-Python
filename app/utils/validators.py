def is_valid_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro segundo algoritmo oficial.
    
    Args:
        cpf: String contendo CPF (aceita formatação com pontos e hífen)
        
    Returns:
        True se o CPF é válido, False C.C.
        
    """
    # Remove caracteres não numéricos
    cpf = "".join(filter(str.isdigit, cpf))
    
    # Verifica tamanho
    if len(cpf) != 11:
        return False
    
    # Rejeita CPFs com todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return False
    
    def calculate_digit(cpf_slice: str, initial_factor: int) -> int:
        """
        Calcula dígito verificador usando algoritmo oficial do CPF.
        
        Args:
            cpf_slice: Slice do CPF para calcular (9 ou 10 dígitos)
            initial_factor: Fator inicial (10 para 1º dígito, 11 para 2º)
            
        Returns:
            Dígito verificador calculado (0-9)
        """
        total = sum(
            int(digit) * (initial_factor - index) 
            for index, digit in enumerate(cpf_slice)
        )
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Calcula e valida os dígitos verificadores
    digit1 = calculate_digit(cpf[:9], 10)
    digit2 = calculate_digit(cpf[:10], 11)
    
    return cpf[-2:] == f"{digit1}{digit2}"