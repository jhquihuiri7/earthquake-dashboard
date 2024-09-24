window.onload = function() {
    Swal.fire({
        width:"80%",
        title: "Terremotos Mundiales",
        html: `
            <p style="font-size: 16px;">
        El <strong>dashboard</strong> muestra datos de <strong>terremotos</strong> ocurridos entre <strong>1995</strong> y <strong>2023</strong>, incluyendo detalles como
        <strong>título</strong>, <strong>magnitud</strong>, <strong>fecha/hora</strong>, <strong>intensidad</strong>, <strong>alerta</strong>, <strong>eventos de tsunami</strong>,
        <strong>distancia</strong>, <strong>profundidad</strong>, <strong>coordenadas</strong>, <strong>localización</strong>, <strong>continente</strong> y <strong>país</strong>.
    </p>
    <br></br>
    <p style="font-size: 16px;">
        Se visualizan estos eventos en un <strong>mapa</strong>, aplicando <strong>filtros</strong> de <strong>magnitud</strong> y <strong>riesgo de tsunami</strong>. También se ofrece
        información general como la <strong>magnitud máxima</strong>, <strong>profundidad promedio</strong> y el <strong>total de eventos registrados</strong>, destacando que
        <strong>Indonesia</strong>, <strong>Papua Nueva Guinea</strong> y <strong>Chile</strong> son los <strong>países</strong> con más <strong>terremotos</strong>. El <strong>dataset</strong>
        incluye <strong>valores faltantes</strong> que han sido analizados y reemplazados.
    </p>
            `,
        confirmButtonText:"Ir al dashboard"
    });
};