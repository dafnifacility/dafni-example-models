import sys
import numpy as np
import pandas as pd
 
try:
    import netCDF4 as nc
except ImportError:
    sys.exit("Missing dependency: pip install netCDF4")
 
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
 
console = Console() if HAS_RICH else None
 
 
# ── Helpers ────────────────────────────────────────────────────────────────────
 
def separator(title=""):
    width = 70
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * pad}")
    else:
        print("─" * width)
 
 
def fmt_shape(shape):
    return " × ".join(str(s) for s in shape) if shape else "scalar"
 
 
def fmt_value(val):
    """Condense an array into a readable one-liner."""
    if np.isscalar(val):
        return str(val)
    val = np.asarray(val)
    if val.ndim == 0:
        return str(val.item())
    if val.size <= 6:
        return str(val.tolist())
    return f"[{val.flat[0]:.4g}, {val.flat[1]:.4g}, … {val.flat[-1]:.4g}]"
 
 
# ── Overview ───────────────────────────────────────────────────────────────────
 
def print_overview(ds):
    """Print high-level file metadata."""
    title = f"NetCDF File Overview"
    attrs = {k: getattr(ds, k) for k in ds.ncattrs()} if ds.ncattrs() else {}
 
    if HAS_RICH:
        panel_lines = []
        panel_lines.append(f"[bold]Format:[/bold]       {ds.file_format}")
        panel_lines.append(f"[bold]Dimensions:[/bold]   {len(ds.dimensions)}")
        panel_lines.append(f"[bold]Variables:[/bold]    {len(ds.variables)}")
        panel_lines.append(f"[bold]Groups:[/bold]       {len(ds.groups)}")
        if attrs:
            panel_lines.append("")
            panel_lines.append("[bold underline]Global attributes[/bold underline]")
            for k, v in attrs.items():
                panel_lines.append(f"  [cyan]{k}[/cyan]: {v}")
        console.print(Panel("\n".join(panel_lines), title=f"[bold green]{title}[/bold green]", expand=False))
    else:
        separator("OVERVIEW")
        print(f"  Format     : {ds.file_format}")
        print(f"  Dimensions : {len(ds.dimensions)}")
        print(f"  Variables  : {len(ds.variables)}")
        print(f"  Groups     : {len(ds.groups)}")
        if attrs:
            print("\n  Global attributes:")
            for k, v in attrs.items():
                print(f"    {k}: {v}")
 
 
# ── Dimensions ─────────────────────────────────────────────────────────────────
 
def print_dimensions(ds):
    if HAS_RICH:
        table = Table(title="Dimensions", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Size", justify="right")
        table.add_column("Unlimited")
        for name, dim in ds.dimensions.items():
            table.add_row(name, str(dim.size), "✓" if dim.isunlimited() else "")
        console.print(table)
    else:
        separator("DIMENSIONS")
        print(f"  {'Name':<20} {'Size':>10}  Unlimited")
        print(f"  {'─'*20} {'─'*10}  {'─'*9}")
        for name, dim in ds.dimensions.items():
            flag = "✓" if dim.isunlimited() else ""
            print(f"  {name:<20} {dim.size:>10}  {flag}")
 
 
# ── Variables ──────────────────────────────────────────────────────────────────
 
def print_variables(ds):
    if HAS_RICH:
        table = Table(title="Variables", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Dtype", style="yellow")
        table.add_column("Shape")
        table.add_column("Dims")
        table.add_column("Units")
        table.add_column("Long name / Description")
        for name, var in ds.variables.items():
            units = getattr(var, "units", "—")
            long  = getattr(var, "long_name", getattr(var, "description", "—"))
            table.add_row(
                name,
                str(var.dtype),
                fmt_shape(var.shape),
                ", ".join(var.dimensions),
                units,
                str(long)[:60],
            )
        console.print(table)
    else:
        separator("VARIABLES")
        fmt = "  {:<20} {:<10} {:<20} {:<30} {:<12} {}"
        print(fmt.format("Name", "Dtype", "Shape", "Dims", "Units", "Long name"))
        print(fmt.format("─"*20, "─"*10, "─"*20, "─"*30, "─"*12, "─"*30))
        for name, var in ds.variables.items():
            units = getattr(var, "units", "—")
            long  = getattr(var, "long_name", getattr(var, "description", "—"))
            print(fmt.format(
                name[:20],
                str(var.dtype)[:10],
                fmt_shape(var.shape)[:20],
                ", ".join(var.dimensions)[:30],
                str(units)[:12],
                str(long)[:40],
            ))
 
 
# ── Single variable detail ─────────────────────────────────────────────────────
 
def print_variable_detail(ds, var_name):
    if var_name not in ds.variables:
        print(f"\n⚠  Variable '{var_name}' not found. Available: {list(ds.variables.keys())}")
        return
 
    var = ds.variables[var_name]
    data = var[:]
 
    # ── Metadata ──
    if HAS_RICH:
        lines = [
            f"[bold]Dtype:[/bold]        {var.dtype}",
            f"[bold]Shape:[/bold]        {fmt_shape(var.shape)}",
            f"[bold]Dimensions:[/bold]   {', '.join(var.dimensions)}",
        ]
        for attr in var.ncattrs():
            lines.append(f"[cyan]{attr}:[/cyan]  {getattr(var, attr)}")
        console.print(Panel("\n".join(lines), title=f"[bold green]Variable: {var_name}[/bold green]", expand=False))
    else:
        separator(f"VARIABLE: {var_name}")
        print(f"  Dtype      : {var.dtype}")
        print(f"  Shape      : {fmt_shape(var.shape)}")
        print(f"  Dimensions : {', '.join(var.dimensions)}")
        for attr in var.ncattrs():
            print(f"  {attr:<12}: {getattr(var, attr)}")
 
    # ── Stats ──
    flat = data.compressed() if np.ma.is_masked(data) else data.ravel()
    flat = flat.astype(float)
 
    if flat.size == 0:
        print("  (no unmasked data)")
        return
 
    stats = {
        "count": flat.size,
        "min":   float(np.nanmin(flat)),
        "max":   float(np.nanmax(flat)),
        "mean":  float(np.nanmean(flat)),
        "std":   float(np.nanstd(flat)),
        "NaNs":  int(np.sum(np.isnan(flat))),
    }
 
    if HAS_RICH:
        table = Table(title="Statistics", header_style="bold magenta")
        for col in stats:
            table.add_column(col, justify="right")
        table.add_row(*[f"{v:,.4g}" if isinstance(v, float) else f"{v:,}" for v in stats.values()])
        console.print(table)
    else:
        separator("STATISTICS")
        for k, v in stats.items():
            print(f"  {k:<8}: {v:,.4g}" if isinstance(v, float) else f"  {k:<8}: {v:,}")
 
    # ── Sample values ──
    if data.ndim == 1 and data.size <= 50:
        df = pd.DataFrame({"index": range(data.size), var_name: data})
        if HAS_RICH:
            console.print("\n[bold]All values:[/bold]")
            console.print(df.to_string(index=False))
        else:
            separator("ALL VALUES")
            print(df.to_string(index=False))
 
    elif data.ndim == 2:
        rows, cols = min(6, data.shape[0]), min(6, data.shape[1])
        snippet = pd.DataFrame(data[:rows, :cols])
        if HAS_RICH:
            console.print(f"\n[bold]First {rows}×{cols} slice:[/bold]")
            console.print(snippet.to_string())
        else:
            separator(f"FIRST {rows}×{cols} SLICE")
            print(snippet.to_string())
 
    else:
        if HAS_RICH:
            console.print(f"\n[bold]First few values:[/bold] {fmt_value(data)}")
        else:
            separator("SAMPLE VALUES")
            print(f"  {fmt_value(data)}")
 
 
# ── Entry point ────────────────────────────────────────────────────────────────
 
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
 
    path     = sys.argv[1]
    var_name = sys.argv[2] if len(sys.argv) > 2 else None
 
    try:
        ds = nc.Dataset(path, "r")
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")
    except Exception as e:
        sys.exit(f"Could not open file: {e}")
 
    print_overview(ds)
    print_dimensions(ds)
    print_variables(ds)
 
    if var_name:
        print_variable_detail(ds, var_name)
    else:
        # Auto-detail any 1D coordinate variables (time, lat, lon, etc.)
        coord_hints = {"time", "lat", "lon", "latitude", "longitude", "level", "depth", "height", "lev"}
        for name in ds.variables:
            var = ds.variables[name]
            if name.lower() in coord_hints and var.ndim == 1 and var.size <= 100:
                print_variable_detail(ds, name)
                break  # just show one for the overview
 
    ds.close()
 
 
if __name__ == "__main__":
    main()