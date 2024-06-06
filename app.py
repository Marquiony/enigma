import streamlit as st

st.write(""" 
# Bem vindo a criptografia da máquina enigma
""")

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def set_position(self, pos):
        self.position = (ord(pos.upper()) - ord('A')) % 26

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch

    def encrypt_forward(self, c):
        idx = (ord(c) - ord('A') + self.position) % 26
        encrypted_char = self.wiring[idx]
        return chr((ord(encrypted_char) - ord('A') - self.position + 26) % 26 + ord('A'))

    def encrypt_backward(self, c):
        idx = (ord(c) - ord('A') + self.position) % 26
        encrypted_char = chr((self.wiring.index(chr(idx + ord('A'))) - self.position + 26) % 26 + ord('A'))
        return encrypted_char

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, c):
        return self.wiring[ord(c) - ord('A')]

class Plugboard:
    def __init__(self, wiring):
        self.wiring = wiring

    def swap(self, c):
        return self.wiring.get(c, c)

class Enigma:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def set_rotor_positions(self, positions):
        for rotor, pos in zip(self.rotors, positions):
            rotor.set_position(pos)

    def encrypt(self, message):
        encrypted_message = ''
        for c in message:
            if c.isalpha():
                c = c.upper()
                c = self.plugboard.swap(c)
                for rotor in self.rotors:
                    c = rotor.encrypt_forward(c)
                c = self.reflector.reflect(c)
                for rotor in reversed(self.rotors):
                    c = rotor.encrypt_backward(c)
                c = self.plugboard.swap(c)
                encrypted_message += c
                for rotor in self.rotors:
                    if not rotor.rotate():
                        break
            else:
                encrypted_message += c
        return encrypted_message

# Configuração de exemplo
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 17)  # Rotor I
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 5)   # Rotor II
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 22)  # Rotor III
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")  # Reflector B
plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})  # Exemplo de plugboard

enigma = Enigma([rotor1, rotor2, rotor3], reflector, plugboard)

# Interface do Streamlit
st.title("Máquina Enigma")

# Entrada da posição inicial dos rotores
initial_positions = st.text_input("Digite a posição inicial dos rotores (por exemplo, ABC):").upper()

# Caixa de texto para a mensagem a ser criptografada
message_encrypt = st.text_area("Digite a mensagem para criptografar:")

# Botão para criptografar
if st.button("Criptografar"):
    if initial_positions and message_encrypt:
        enigma.set_rotor_positions(initial_positions)
        encrypted_message = enigma.encrypt(message_encrypt)
        st.write(f"Mensagem Criptografada: {encrypted_message}")
    else:
        st.write("Por favor, insira a posição inicial dos rotores e a mensagem para criptografar.")

# Caixa de texto para a mensagem a ser descriptografada
message_decrypt = st.text_area("Digite a mensagem para descriptografar:")

# Botão para descriptografar
if st.button("Descriptografar"):
    if initial_positions and message_decrypt:
        enigma.set_rotor_positions(initial_positions)
        decrypted_message = enigma.encrypt(message_decrypt)  # A criptografia Enigma é reversível com as mesmas configurações
        st.write(f"Mensagem Descriptografada: {decrypted_message}")
    else:
        st.write("Por favor, insira a posição inicial dos rotores e a mensagem para descriptografar.")
