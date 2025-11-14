const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('file');
const status = document.getElementById('status');
const progress = document.getElementById('progress');
const log = document.getElementById('log');
const refreshBtn = document.getElementById('refresh');
const productTableBody = document.querySelector('#productTable tbody');
const filterSku = document.getElementById('filterSku');
const deleteAllBtn = document.getElementById('deleteAll');

uploadBtn.onclick = async () => {
  const file = fileInput.files[0];
  if (!file) { alert('pick a CSV'); return; }
  const form = new FormData();
  form.append('file', file);
  status.innerText = 'Uploading...';
  progress.value = 5;
  const res = await fetch('/upload', { method: 'POST', body: form });
  const data = await res.json();
  if (!data.job_id) { status.innerText = 'Upload failed'; return; }
  status.innerText = 'Uploaded. Job: ' + data.job_id;
  pollJob(data.job_id);
};

async function pollJob(jobId) {
  status.innerText = 'Processing...';
  const interval = setInterval(async () => {
    try {
      const res = await fetch('/jobs/' + jobId);
      const j = await res.json();
      if (j.error) { status.innerText = 'Job not found'; clearInterval(interval); return; }
      const total = j.total_rows || 0;
      const processed = j.processed_rows || 0;
      let pct = total ? Math.floor((processed / total) * 100) : 0;
      progress.value = pct;
      log.innerText = `Status: ${j.status} — ${processed}/${total}`;
      if (j.status === 'SUCCESS' || j.status === 'FAILED') {
        status.innerText = 'Finished: ' + j.status;
        clearInterval(interval);
        fetchProducts();
      }
    } catch (e) {
      console.error(e);
      clearInterval(interval);
    }
  }, 1500);
}

async function fetchProducts() {
  const q = filterSku.value || '';
  const res = await fetch('/products?limit=50&skip=0&filter=' + encodeURIComponent(q));
  if (!res.ok) return;
  const data = await res.json();
  productTableBody.innerHTML = '';
  (data.items || []).forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${p.id}</td><td>${p.sku}</td><td>${p.name||''}</td><td>${p.price||''}</td><td>${p.active}</td>`;
    productTableBody.appendChild(tr);
  });
}

refreshBtn.onclick = fetchProducts;

deleteAllBtn.onclick = async () => {
  if (!confirm("Are you sure? This cannot be undone.")) return;
  const res = await fetch('/products/delete_all', { method: 'POST' });
  const j = await res.json();
  alert('Deleted ' + (j.deleted || 0) + ' products');
  fetchProducts();
};

// initial load
fetchProducts();
