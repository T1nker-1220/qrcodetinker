#!/usr/bin/env python
"""
QR Code Generator CLI.

A command-line interface for generating QR codes from various input types.
"""

import os
import sys
import click
from typing import Optional, Tuple

from qr_generator import QRGenerator
from qr_generator.utils import (
    detect_content_type,
    format_wifi_data,
    format_contact_data,
)


@click.group()
def cli():
    """QR Code Generator CLI."""
    pass


@cli.command()
@click.option("--content", required=True, help="Content to encode in the QR code")
@click.option("--output", required=True, help="Output file path")
@click.option("--title", help="Title to display above the QR code")
@click.option("--version", type=int, help="QR code version (1-40)")
@click.option("--box-size", type=int, help="Size of each box in pixels")
@click.option("--border", type=int, help="Border size in boxes")
@click.option("--fg-color", help="Foreground color (color of the QR code)")
@click.option("--bg-color", help="Background color")
def generate(
    content: str,
    output: str,
    title: Optional[str] = None,
    version: Optional[int] = None,
    box_size: Optional[int] = None,
    border: Optional[int] = None,
    fg_color: Optional[str] = None,
    bg_color: Optional[str] = None,
):
    """Generate a QR code from the given content."""
    try:
        qr = QRGenerator()
        output_path = qr.generate(
            content=content,
            output_path=output,
            title=title,
            version=version,
            box_size=box_size,
            border=border,
            fg_color=fg_color,
            bg_color=bg_color,
        )
        click.echo(f"QR code generated successfully: {output_path}")
        
        # Detect and display content type
        content_type = detect_content_type(content)
        click.echo(f"Content type detected: {content_type}")
        
    except Exception as e:
        click.echo(f"Error generating QR code: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--content", required=True, help="Content to encode in the QR code")
@click.option("--output", required=True, help="Output file path")
@click.option("--logo", required=True, help="Logo image path")
@click.option("--title", help="Title to display above the QR code")
@click.option("--logo-size", type=float, default=0.2, help="Logo size as a fraction of QR code size (0.0-1.0)")
@click.option("--version", type=int, help="QR code version (1-40)")
@click.option("--box-size", type=int, help="Size of each box in pixels")
@click.option("--border", type=int, help="Border size in boxes")
@click.option("--fg-color", help="Foreground color (color of the QR code)")
@click.option("--bg-color", help="Background color")
def generate_with_logo(
    content: str,
    output: str,
    logo: str,
    title: Optional[str] = None,
    logo_size: float = 0.2,
    version: Optional[int] = None,
    box_size: Optional[int] = None,
    border: Optional[int] = None,
    fg_color: Optional[str] = None,
    bg_color: Optional[str] = None,
):
    """Generate a QR code with a logo in the center."""
    try:
        qr = QRGenerator()
        output_path = qr.generate_with_logo(
            content=content,
            output_path=output,
            logo_path=logo,
            title=title,
            logo_size=logo_size,
            version=version,
            box_size=box_size,
            border=border,
            fg_color=fg_color,
            bg_color=bg_color,
        )
        click.echo(f"QR code with logo generated successfully: {output_path}")
        
        # Detect and display content type
        content_type = detect_content_type(content)
        click.echo(f"Content type detected: {content_type}")
        
    except Exception as e:
        click.echo(f"Error generating QR code with logo: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--ssid", required=True, help="WiFi network name")
@click.option("--password", help="WiFi password")
@click.option("--security", type=click.Choice(["WPA", "WEP", "nopass"]), default="WPA", help="Security type")
@click.option("--output", required=True, help="Output file path")
@click.option("--title", help="Title to display above the QR code")
@click.option("--logo", help="Logo image path (optional)")
@click.option("--version", type=int, help="QR code version (1-40)")
@click.option("--box-size", type=int, help="Size of each box in pixels")
def wifi(
    ssid: str,
    password: Optional[str],
    security: str,
    output: str,
    title: Optional[str] = None,
    logo: Optional[str] = None,
    version: Optional[int] = None,
    box_size: Optional[int] = None,
):
    """Generate a WiFi network QR code."""
    try:
        # Format WiFi data
        wifi_data = format_wifi_data(ssid, password, security)
        
        qr = QRGenerator()
        
        if logo:
            output_path = qr.generate_with_logo(
                content=wifi_data,
                output_path=output,
                logo_path=logo,
                title=title or f"WiFi: {ssid}",
                version=version,
                box_size=box_size,
            )
        else:
            output_path = qr.generate(
                content=wifi_data,
                output_path=output,
                title=title or f"WiFi: {ssid}",
                version=version,
                box_size=box_size,
            )
            
        click.echo(f"WiFi QR code generated successfully: {output_path}")
        
    except Exception as e:
        click.echo(f"Error generating WiFi QR code: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--name", required=True, help="Contact name")
@click.option("--phone", help="Phone number")
@click.option("--email", help="Email address")
@click.option("--company", help="Company name")
@click.option("--job-title", help="Job title")
@click.option("--website", help="Website URL")
@click.option("--output", required=True, help="Output file path")
@click.option("--qr-title", help="Title to display above the QR code")
@click.option("--logo", help="Logo image path (optional)")
@click.option("--version", type=int, help="QR code version (1-40)")
@click.option("--box-size", type=int, help="Size of each box in pixels")
def contact(
    name: str,
    phone: Optional[str],
    email: Optional[str],
    company: Optional[str],
    job_title: Optional[str],
    website: Optional[str],
    output: str,
    qr_title: Optional[str] = None,
    logo: Optional[str] = None,
    version: Optional[int] = None,
    box_size: Optional[int] = None,
):
    """Generate a contact information QR code (vCard)."""
    try:
        # Format contact data as vCard
        vcard_data = format_contact_data(
            name=name,
            phone=phone,
            email=email,
            company=company,
            title=job_title,
            website=website,
        )
        
        qr = QRGenerator()
        
        if logo:
            output_path = qr.generate_with_logo(
                content=vcard_data,
                output_path=output,
                logo_path=logo,
                title=qr_title or f"Contact: {name}",
                version=version,
                box_size=box_size,
            )
        else:
            output_path = qr.generate(
                content=vcard_data,
                output_path=output,
                title=qr_title or f"Contact: {name}",
                version=version,
                box_size=box_size,
            )
            
        click.echo(f"Contact QR code generated successfully: {output_path}")
        
    except Exception as e:
        click.echo(f"Error generating contact QR code: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
