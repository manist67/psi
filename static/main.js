function polyToText(rq) {
    return rq.poly.reduce((prev, c, idx) => {
        const x = rq.poly.length != idx + 1 ? ` * x^${rq.poly.length - idx - 1}` : "";
        return prev + ` ${c>=0 ? "+" : "-" } ${Math.abs(c)}${x}`
    }, "(") + `) % ${rq.q}`;
}

$(()=>{
    const clientData = [];
    const serverData = [];

    function refreshClientMessages() {
        const $wrapper = $(".div-message.div-client");
        $wrapper.empty();
        for(let datum of clientData) {
            const $row = $("<div/>", {
                class: "row-data div-client-data",
                "data-value": datum
            });

            $row.append($("<span/>", {
                text: datum
            }));

            $wrapper.append($row)
        }
    }

    function refreshServerMessages() {
        const $wrapper = $(".div-message.div-server");
        $wrapper.empty();
        for(let datum of serverData) {
            const $row = $("<div/>", {
                class: "row-data div-server-data",
                "data-value": datum
            });

            $row.append($("<span/>", {
                text: datum
            }));

            $wrapper.append($row)
        }

    }

    $(document).on( "click", ".div-client-data", function () {
        const $this = $(this);
        const val = Number($this.attr("data-value"));

        const i = clientData.indexOf(val);
        if (i !== -1) clientData.splice(i, 1);
        refreshClientMessages();
    })

    $(document).on( "click", ".div-server-data", function () {
        const $this = $(this);
        const val = Number($this.attr("data-value"));

        const i = serverData.indexOf(val);
        if (i !== -1) serverData.splice(i, 1);
        refreshServerMessages();
    })

    $("#btn-client").click(()=>{
        const $input = $("#input-client");
        const val = Number($input.val())
        if(!val) return;

        if(!clientData.includes(val)) clientData.push(val);
        $input.val(null);
        refreshClientMessages();
    })

    $("#btn-server").click(()=>{
        const $input = $("#input-server");
        const val = Number($input.val())
        if(!val) return;

        if(!serverData.includes(val)) serverData.push(val);
        $input.val(null);
        refreshServerMessages();
    });

    $("#btn-generate-key").click(async () => {
        const { data } = await axios.get("/keys");
        const { public_key,  secret_key } = data;

        const p0 = polyToText(public_key[0]);
        const p1 = polyToText(public_key[1]);
        const s = polyToText(secret_key);
    
        $(".public-key.a0").text(p0)
        $(".public-key.a1").text(p1)
        $(".secret-key").text(s)
    });

    $("#btn-client-encrypt").click(async () => {
        const { data } = await axios.post("/encrypt_client", {
            data: clientData
        });
        const $wrapper = $(".div-cipher-client");
        $wrapper.empty();
        for(let i in clientData) {
            const [a0, a1] = data[i];
            const $row = $("<div/>", {
                class: "div-encrypt-row"
            });

            $row.append($("<p/>", { text: clientData[i], "class": "p-origin" }));
            $row.append($("<p/>", { text: "a0 : " + polyToText(a0) }));
            $row.append($("<p/>", { text: "a1 : " + polyToText(a1) }));
    
            $wrapper.append($row)
        }
    });
    
    $("#btn-random-number-server").click(async () => {
        for(let i = 0; i < 10; i++) {
            const v = Math.round(Math.random() * 100);
            if(serverData.includes(v)) continue;
            serverData.push(v)
        }

        refreshServerMessages()
    });

    $("#btn-server-encrypt").click(async () => {
        const { data } = await axios.post("/encrypt_server", {
            data: serverData
        });
        const $wrapper = $(".div-cipher-server");
        $wrapper.empty();
        for(let i in serverData) {
            const [a0, a1] = data[i];
            const $row = $("<div/>", {
                class: "div-encrypt-row"
            });

            $row.append($("<p/>", { text: serverData[i], "class": "p-origin" }));
            $row.append($("<p/>", { text: "a0 : " + polyToText(a0) }));
            $row.append($("<p/>", { text: "a1 : " + polyToText(a1) }));
    
            $wrapper.append($row)
        }
    });

    $("#btn-intersection").click(async () => {
        const { data } = await axios.get("/intersection");
        const $wrapper = $(".intersection-wrapper");
        $wrapper.empty()
        let i = 0;
        for(let result of data ) {
            i+=1;
            const [ a0, a1 ] = result;
            const $row = $("<div/>", { class: "div-encrypt-row" });
            
            $row.append($("<p/>", { text: i, class: "p-origin" }));
            $row.append($("<p/>", { text: "a0 : " + polyToText(a0) }));
            $row.append($("<p/>", { text: "a1 : " + polyToText(a1) }));
    
            $wrapper.append($row)
        }
    });

    $("#btn-decrypt-client").click(async () => {
        const { data } = await axios.post("/decrypt_client", {
            data: clientData
        });

        const { exists, decrypted } = data;
        const $wrapper = $(".intersection-decrypt-wrapper");
        $wrapper.empty()

        let i = 0, j = 0;
        for(let result of decrypted ) {
            if(i != 0 && i % serverData.length == 0) {
                $wrapper.append($("<div/>", { class: "div-divide"}))
            }
            if(i % serverData.length == 0) {
                $wrapper.append($("<div/>", { class: "div-item", text: clientData[ j++ ] }))
            }
            i++;

            const $row = $("<div/>", { class: "div-result", text: result});
            if(result == 0) $row.addClass("check")
            $wrapper.append($row)
        }
        
        for(let value of exists) {
            console.log($(`.div-client-data[data-value=${value}]`))
            $(`.div-client-data[data-value=${value}]`).addClass("light-on")
        }
    });
})