function trocarTela(atual, proximo){
    const atualT = document.getElementById(atual);
    const proximoT = document.getElementById(proximo);

    atualT.classList.remove("visual");
    atualT.classList.add("escondido");

    proximoT.classList.remove("escondido");
    proximoT.classList.add("visual");
}

async function login(){
    const usuario = document.getElementById("nomeV");
    const senha = document.getElementById("senhaV");

    if (usuario.value.trim() === "" || senha.value.trim() === ""){
        alert("insira dados válidos")
        usuario.value = ""
        senha.value = ""
    } else{
        try{
            const resposta = await fetch("http://127.0.0.1:5000/login",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "nome": usuario.value,
                "senha": senha.value
                })
            })
            const dados = await resposta.json()

            if (resposta.ok){
                localStorage.setItem("usuario_id", dados.id)
                localStorage.setItem("usuario_nome", dados.nome)

                alert("Login realizado com sucesso")
                senha.value = ""

                if (dados.id === 1){
                    window.location.href = "/front end/templates/admin.html"
                }
                else{
                    window.location.href = "/front end/templates/index.html"
                }
            } else if (resposta.status === 404){
                alert("Usuario não encontrado")
                usuario.value = ""
                senha.value = ""
            } else if (resposta.status === 401){
                alert("Senha incorreta")
                usuario.value = ""
                senha.value = ""
            }
        } catch (erro){
            alert("Erro ao conectar com o servidor, tente novamente")
            usuario.value = ""
            senha.value = ""
        }
    }
}

async function cadastro() {
    const nome = document.getElementById("nomeC")
    const email = document.getElementById("emailC")
    const senha = document.getElementById("senhaC")

    if(nome.value.trim() === "" || email.value.trim() === "" || senha.value.trim() === ""){
        alert("insira dados válidos")
        nome.value = ""
        email.value = ""
        senha.value = ""
    } else {
        try{
            const resposta = await fetch("http://127.0.0.1:5000/cadastro",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify ({
                "nome": nome.value,
                "email": email.value,
                "senha": senha.value
                })
            })
            
            const dados = await resposta.json()

            if (resposta.ok){
                alert("cadastro realizado com sucesso! você será redirecionado para o login")

                window.location.href = "front end/templates/login_cadastro.html"
            } else if (resposta.status === 500){
                alert("erro ao conectar com o servidor")
                nome.value = ""
                email.value = ""
                senha.value = ""
            } else if (resposta.status === 409){
                alert("usuário já existente")
            }
        } catch (erro){
            alert("erro ao conectar com o servidor")
        }
    }
}

const saudacao = document.getElementById("saudacao")
const nome = localStorage.getItem("usuario_nome")

saudacao.innerText = "Bem vindo, " + nome

const id = localStorage.getItem("usuario_id")

const notificacoes = await fetch("http://127.0.0.1:5000/notificacoes/<int:id>", {
    
     

})