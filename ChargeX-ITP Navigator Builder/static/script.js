document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ DOMContentLoaded fired");

  fetch('/tree')
    .then(response => {
      console.log("✅ /tree fetch status:", response.status);
      return response.json();
    })
    .then(data => {
      console.log("✅ /tree data received:", data);

      $('#tree').jstree({
        'core': {
          'data': data
        }
      });

      console.log("✅ jsTree init called");

      $('#tree').on("select_node.jstree", function (e, data) {
        console.log("✅ Node selected:", data.node);

        const filename = data.node.li_attr['data-filename'];
        if (filename) {
          console.log(`✅ Fetching test case file: ${filename}`);

          fetch(`/testcases/${filename}`)
            .then(res => {
              console.log(`✅ /testcases/${filename} fetch status:`, res.status);
              return res.text();
            })
            .then(html => {
              const contentDiv = document.getElementById('content');
              contentDiv.innerHTML = html;

              // Button container
              const buttonContainer = document.createElement('div');
              buttonContainer.style.marginTop = '20px';
              buttonContainer.style.display = 'flex';
              buttonContainer.style.gap = '10px';

              // Print button
              const printButton = document.createElement('button');
              printButton.textContent = '🖨️ Print Test Table';
              printButton.style.padding = '10px 20px';
              printButton.style.fontSize = '14px';
              printButton.style.cursor = 'pointer';
              printButton.classList.add('no-print');

              // Download button
              const downloadButton = document.createElement('button');
              downloadButton.textContent = '💾 Download All Test Tables';
              downloadButton.style.padding = '10px 20px';
              downloadButton.style.fontSize = '14px';
              downloadButton.style.cursor = 'pointer';
              downloadButton.classList.add('no-print');

              printButton.addEventListener('click', function () {
                const table = contentDiv.querySelector('table');
                if (table) {
                  const printWindow = window.open('', '', 'height=800,width=1000');
                  printWindow.document.write('<html><head><title>Print Test Table</title>');

                  // Link CSS for consistent style
                  printWindow.document.write(
                    `<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
                     <link rel="stylesheet" href="/static/style.css">`
                  );

                  // Inline print-specific CSS to fit content on one page
                  printWindow.document.write(`
                    <style>
                      * { box-sizing: border-box; }
                      body { font-family: Arial, sans-serif; margin: 0; padding: 1rem; }
                      table { width: 100%; border-collapse: collapse; font-size: 12px; }
                      td, th { padding: 4px; border: 1px solid #000; vertical-align: top; }
                      img { max-width: 100%; height: auto; }
                      .no-print { display: none; }
                      @media print {
                        body { zoom: 80%; } /* shrink content slightly to fit page */
                      }
                    </style>
                  `);

                  printWindow.document.write('</head><body>');
                  printWindow.document.write(contentDiv.innerHTML);
                  printWindow.document.write('</body></html>');
                  printWindow.document.close();
                  printWindow.focus();
                  printWindow.print();
                } else {
                  alert('No table found to print!');
                }
              });

              downloadButton.addEventListener('click', function () {
                const link = document.createElement('a');
                link.href = '/static/EEITP.pdf';
                link.download = 'EEITP.pdf';
                link.click();
              });

              buttonContainer.appendChild(printButton);
              buttonContainer.appendChild(downloadButton);
              contentDiv.appendChild(buttonContainer);
            })
            .catch(err => {
              console.error(`❌ Error fetching /testcases/${filename}:`, err);
            });
        } else {
          console.warn("⚠️ Selected node has no data-filename attribute");
        }
      });
    })
    .catch(err => {
      console.error("❌ Error fetching /tree:", err);
    });
});
