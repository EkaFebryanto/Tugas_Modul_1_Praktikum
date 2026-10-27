# src/main.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models import DaftarMahasiswa, Mahasiswa

console = Console()
db = DaftarMahasiswa()


def tampilkan_menu():
    """Tampilkan menu utama."""
    menu_text = (
        "[bold cyan]Sistem Informasi Mahasiswa[/]\n\n"
        "1. Tambah Mahasiswa\n"
        "2. Tampilkan Semua Mahasiswa\n"
        "3. Cari Mahasiswa (NIM)\n"
        "4. Hapus Mahasiswa\n"
        "5. Edit IPK Mahasiswa\n"
        "0. Keluar"
    )
    console.print(Panel(menu_text, title="Menu", border_style="cyan"))


def tambah_mahasiswa():
    """Form tambah mahasiswa baru."""
    console.print("\n[bold]Tambah Mahasiswa Baru[/]")
    nim = console.input("  NIM: ")
    nama = console.input("  Nama: ")
    prodi = console.input("  Program Studi: ")
    angkatan = int(console.input("  Angkatan: "))
    ipk = float(console.input("  IPK: "))
    try:
        mhs = Mahasiswa(nim, nama, prodi, angkatan, ipk)
        db.tambah(mhs)
        console.print(f"  [green]Berhasil: {nama} ditambahkan[/]")
    except ValueError as e:
        console.print(f"  [red]Gagal: {e}[/]")


def tampilkan_semua():
    """Tampilkan seluruh data dalam tabel."""
    if not db.data:
        console.print("[yellow]Belum ada data mahasiswa.[/]")
        return
    table = Table(title="Daftar Mahasiswa")
    table.add_column("NIM", style="cyan")
    table.add_column("Nama")
    table.add_column("Program Studi")
    table.add_column("Angkatan", justify="right")
    table.add_column("IPK", justify="right")
    for m in db.data:
        table.add_row(m.nim, m.nama, m.program_studi, str(m.angkatan), f"{m.ipk:.2f}")
    console.print(table)


def cari_mahasiswa():
    """Cari mahasiswa berdasarkan NIM dan tampilkan hasilnya."""
    console.print("\n[bold]Cari Mahasiswa[/]")
    nim = console.input("  NIM: ").strip()
    mhs = db.cari(nim)
    if mhs is None:
        console.print(f"  [yellow]Mahasiswa dengan NIM {nim} tidak ditemukan.[/]")
        return
    table = Table(title="Hasil Pencarian")
    table.add_column("NIM", style="cyan")
    table.add_column("Nama")
    table.add_column("Program Studi")
    table.add_column("Angkatan", justify="right")
    table.add_column("IPK", justify="right")
    table.add_row(mhs.nim, mhs.nama, mhs.program_studi, str(mhs.angkatan), f"{mhs.ipk:.2f}")
    console.print(table)


def hapus_mahasiswa():
    """Hapus mahasiswa berdasarkan NIM."""
    console.print("\n[bold]Hapus Mahasiswa[/]")
    nim = console.input("  NIM: ").strip()
    if db.hapus(nim):
        console.print(f"  [green]Berhasil: data NIM {nim} dihapus[/]")
    else:
        console.print(f"  [red]Gagal: NIM {nim} tidak ditemukan[/]")


def edit_ipk():
    """Perbarui IPK mahasiswa berdasarkan NIM (validasi 0.0-4.0)."""
    console.print("\n[bold]Edit IPK Mahasiswa[/]")
    nim = console.input("  NIM: ").strip()
    try:
        ipk_baru = float(console.input("  IPK baru: "))
        if db.edit_ipk(nim, ipk_baru):
            console.print(f"  [green]Berhasil: IPK NIM {nim} diubah menjadi {ipk_baru:.2f}[/]")
        else:
            console.print(f"  [red]Gagal: NIM {nim} tidak ditemukan[/]")
    except ValueError as e:
        console.print(f"  [red]Gagal: {e}[/]")


def main():
    """Loop utama aplikasi."""
    while True:
        tampilkan_menu()
        pilihan = console.input("\nPilih [0-5]: ")
        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_mahasiswa()
        elif pilihan == "4":
            hapus_mahasiswa()
        elif pilihan == "5":
            edit_ipk()
        elif pilihan == "0":
            console.print("[bold]Sampai jumpa![/]")
            break
        else:
            console.print("[red]Pilihan tidak valid[/]")


if __name__ == "__main__":
    main()
