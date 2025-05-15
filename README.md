# Automasked ROC Plotter

This tool generates graphical plots of **automasked Pixel ROCs** in the CMS detector. It is intended for internal use by the CMS Pixel Calibration team.

The main script, `plot_automasked.py`, processes the list of masked ROCs and produces visual plots indicating their location and status within the pixel detector.

---

## Location

The scripts reside in:

```
/pixel/users/Calibrations/
```

---

## Workflow Overview

### Step 1: Generate the Automasked ROC List

Log into the masked ROC summary host and generate the latest masked channel list:

```bash
ssh yourusername@cmsusr
ssh srv-s2b18-37-01
sudo -u pixelpro -H bash -l

cd /nfshome0/pixelpro/TriDAS
source setenv.sh
cd /nfshome0/pixelpro/opstools/masked

python masked_roc_summary.py | tee "/globalscratch/masked_latest.txt"
```

This creates `/globalscratch/masked_latest.txt`, which will be used as input to the plotting script.

---

### Step 2: Run the Plotting Script

Log into the plotting host:

```bash
ssh srv-s2b18-31-01
sudo -u pixelpro -H zsh -l

cd /nfshome0/pixelpro/TriDAS
source setenv.sh
cd /pixel/users/Calibrations

python plot_automasked.py /globalscratch/masked_latest.txt
```

This creates a new directory in `automasked/` with timestamped plots.

---

## Script Usage

### Basic Command

```bash
python plot_automasked.py /path/to/masked_list.txt
```

### Available Flags

| Argument                    | Description |
|----------------------------|-------------|
| `original_list`            | **(Required)** Path to the input file containing the list of masked ROCs. |
| `-blacklisted`             | If set, only ROCs marked as `BLACKLISTED` in the list will be plotted. |
| `-save`                    | If set, retains the intermediate `list.txt` file used for plotting. By default, this file is deleted. |

---

## Example Usage

Plot all masked ROCs:
```bash
python plot_automasked.py /globalscratch/masked_latest.txt
```

Plot only BLACKLISTED ROCs and keep the intermediate list:
```bash
python plot_automasked.py /globalscratch/masked_latest.txt -blacklisted -save
```

---

## Output

Plots and results are saved to a new directory under:

```
automasked/plots_YYYY_MM_DD_HH_MM_SS/
```

Contents include:
- Individual ROC maps (PNG)
- Combined `plots.pdf` file for easy viewing
- (Optionally) the `list.txt` file with expanded ROC entries

---

## Example Output

Each output image corresponds to a detector layer or ring. The plots are based on online coordinates and show the spatial distribution of masked ROCs.

---

## Authors

- Plotting Engine: Based on work by Paul Schuetze  
- Contributions: Athar Ahmad

---
