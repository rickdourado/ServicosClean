// Variável global para armazenar o texto markdown original
let textoMarkdownOriginal = "";

/**
 * Função principal para processar o texto
 */
async function processarTexto() {
  const textoEntrada = document.getElementById("texto-entrada").value.trim();
  const btnProcessar = document.getElementById("btn-processar");
  const textoSaida = document.getElementById("texto-saida");
  const mensagemErro = document.getElementById("mensagem-erro");
  const downloadButtons = document.getElementById("download-buttons");

  // Validação
  if (!textoEntrada) {
    mostrarErro("Por favor, digite algum texto para processar.");
    return;
  }

  // Limpa mensagens anteriores
  mensagemErro.style.display = "none";
  textoSaida.textContent = "";
  downloadButtons.style.display = "none";
  textoMarkdownOriginal = "";

  // Desabilita o botão e mostra loading
  btnProcessar.disabled = true;
  document.querySelector(".btn-text").style.display = "none";
  document.querySelector(".btn-loader").style.display = "flex";

  try {
    // Faz a requisição para o backend
    const response = await fetch("/processar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        texto: textoEntrada,
      }),
    });

    const data = await response.json();

    if (data.sucesso) {
      // data.resultado agora é um objeto com vários campos
      const resultado = data.resultado;

      // Compõe um Markdown completo a partir dos campos retornados
      const compiledMarkdown = compilarResultadoEmMarkdown(resultado);

      // Armazena o texto markdown original (para download/copiar)
      textoMarkdownOriginal = compiledMarkdown;

      // Converte Markdown para HTML básico e exibe
      const html = converterMarkdownParaHTML(compiledMarkdown);
      textoSaida.innerHTML = html;

      // Mostra os botões de download
      downloadButtons.style.display = "flex";
    } else {
      mostrarErro(data.erro || "Erro ao processar o texto. Tente novamente.");
    }
  } catch (error) {
    console.error("Erro:", error);
    mostrarErro("Erro de conexão. Verifique sua internet e tente novamente.");
  } finally {
    // Reabilita o botão e esconde loading
    btnProcessar.disabled = false;
    document.querySelector(".btn-text").style.display = "inline";
    document.querySelector(".btn-loader").style.display = "none";
  }
}

/**
 * Converte Markdown básico para HTML
 */
function converterMarkdownParaHTML(markdown) {
  if (!markdown) return "";

  let html = markdown;

  // Converte títulos ##
  html = html.replace(/^##\s+(.+)$/gm, "<h2>$1</h2>");

  // Converte negrito **texto**
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Converte listas não ordenadas
  html = html.replace(/^-\s+(.+)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>\n?)+/g, function (match) {
    return "<ul>" + match + "</ul>";
  });

  // Converte listas ordenadas
  html = html.replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");
  // Agrupa listas ordenadas (simplificado)
  html = html.replace(/(<li>.*<\/li>\n?)+/g, function (match) {
    if (match.includes("<ul>")) return match; // Já foi processado
    return "<ol>" + match + "</ol>";
  });

  // Converte quebras de linha em parágrafos
  html = html
    .split("\n\n")
    .map((paragrafo) => {
      paragrafo = paragrafo.trim();
      if (!paragrafo) return "";
      // Se já é um elemento HTML (h2, ul, ol), não envolve em <p>
      if (paragrafo.startsWith("<")) {
        return paragrafo;
      }
      return "<p>" + paragrafo + "</p>";
    })
    .join("\n");

  // Limpa parágrafos vazios
  html = html.replace(/<p><\/p>/g, "");

  return html;
}

/**
 * Mostra mensagem de erro
 */
function mostrarErro(mensagem) {
  const mensagemErro = document.getElementById("mensagem-erro");
  mensagemErro.textContent = mensagem;
  mensagemErro.style.display = "block";

  // Scroll para a mensagem de erro
  mensagemErro.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/**
 * Copia o texto formatado como .txt para a área de transferência
 */
function copiarTexto() {
  if (!textoMarkdownOriginal) {
    mostrarErro("Nenhum resultado disponível para copiar.");
    return;
  }

  // Converte markdown para texto simples (remove formatação)
  const textoSimples = textoMarkdownOriginal
    .replace(/##\s+/g, "") // Remove títulos
    .replace(/\*\*(.+?)\*\*/g, "$1") // Remove negrito
    .replace(/^-\s+/gm, "") // Remove marcadores de lista
    .replace(/^\d+\.\s+/gm, "") // Remove numeração de lista
    .trim();

  // Copia para a área de transferência
  navigator.clipboard
    .writeText(textoSimples)
    .then(function () {
      // Feedback visual
      const btnCopiar = document.getElementById("btn-copiar-texto");
      const textoOriginal = btnCopiar.innerHTML;
      btnCopiar.innerHTML = "<span>✓</span> Copiado!";
      btnCopiar.style.background = "var(--success-color)";
      btnCopiar.style.borderColor = "var(--success-color)";
      btnCopiar.style.color = "white";

      // Restaura o botão após 2 segundos
      setTimeout(function () {
        btnCopiar.innerHTML = textoOriginal;
        btnCopiar.style.background = "";
        btnCopiar.style.borderColor = "";
        btnCopiar.style.color = "";
      }, 2000);
    })
    .catch(function (err) {
      console.error("Erro ao copiar:", err);
      mostrarErro("Erro ao copiar texto. Tente novamente.");
    });
}

/**
 * Baixa o resultado em formato Markdown (.md)
 */
function baixarMarkdown() {
  if (!textoMarkdownOriginal) {
    mostrarErro("Nenhum resultado disponível para download.");
    return;
  }

  const blob = new Blob([textoMarkdownOriginal], {
    type: "text/markdown;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "descricao_servico.md";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Baixa o resultado em formato texto (.txt)
 */
function baixarTexto() {
  if (!textoMarkdownOriginal) {
    mostrarErro("Nenhum resultado disponível para download.");
    return;
  }

  // Converte markdown para texto simples (remove formatação)
  const textoSimples = textoMarkdownOriginal
    .replace(/##\s+/g, "") // Remove títulos
    .replace(/\*\*(.+?)\*\*/g, "$1") // Remove negrito
    .replace(/^-\s+/gm, "") // Remove marcadores de lista
    .replace(/^\d+\.\s+/gm, "") // Remove numeração de lista
    .trim();

  const blob = new Blob([textoSimples], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "descricao_servico.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Compila o objeto de resultado em um único documento Markdown
 */
function compilarResultadoEmMarkdown(res) {
  if (!res || typeof res !== "object") return "";

  const camposOrdem = [
    { key: "descricao_resumida", title: "Descrição Resumida" },
    { key: "descricao_completa", title: "Descrição Completa" },
    { key: "servico_nao_cobre", title: "O que o serviço não cobre" },
    { key: "tempo_atendimento", title: "Tempo para atendimento" },
    { key: "custo", title: "Custo" },
    { key: "resultado_solicitacao", title: "Resultado da solicitação" },
    { key: "documentos_necessarios", title: "Documentos necessários" },
    { key: "instrucoes_solicitante", title: "Instruções para o solicitante" },
    { key: "canais_digitais", title: "Canais digitais" },
    { key: "canais_presenciais", title: "Canais presenciais" },
    { key: "legislacao_relacionada", title: "Legislação relacionada" },
  ];

  let md = "";

  camposOrdem.forEach((c) => {
    const v = res[c.key] || "";
    if (!v || String(v).trim() === "") return; // pula campos vazios

    // Se o campo já tiver títulos Markdown (ex: descricao_completa), preserva
    if (c.key === "descricao_completa") {
      md += `\n\n${v.trim()}\n\n`;
    } else {
      md += `\n\n## ${c.title}\n\n${String(v).trim()}\n\n`;
    }
  });

  return md.trim();
}

/**
 * Permite processar com Enter (Ctrl+Enter)
 */
document.addEventListener("DOMContentLoaded", function () {
  const textoEntrada = document.getElementById("texto-entrada");

  textoEntrada.addEventListener("keydown", function (e) {
    // Ctrl+Enter ou Cmd+Enter para processar
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      processarTexto();
    }
  });
});
